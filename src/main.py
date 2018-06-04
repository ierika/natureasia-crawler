import re
from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from models import db
from models import Url


class MySpider(CrawlSpider):
    """
    Crawls the entire NatureAsia.com.
    Excludes 'zh-tw' website though.
    """
    name = 'natureasia.com'
    allowed_domains = ['natureasia.com']
    start_urls = [
        'https://www.natureasia.com/ja-jp',
        'https://www.natureasia.com/ko-kr',
        'https://www.natureasia.com/en',
    ]
    root_url = 'https://www.natureasia.com'
    languages_regex = r'(ja-jp|en|ko-kr)'
    rules = (
        Rule(
            LinkExtractor(
                allow=r'natureasia\.com/{}'.format(languages_regex),
                deny=(
                    r'natureasia\.com/en/(nmiddleeast|nindia)',
                    r'natureasia\.com/secure',
                ),
            ),
            callback='parse_item',
            follow=True,
        ),
    )

    def parse_item(self, response):
        """
        Update or create database entry.

        If the URL already exist in the database,
        update the priority instead just in case it changed.
        Otherwise, just create an entry.
        """
        referer = response.request.headers.get('Referer', '')
        url = response.url
        language, priority = self.parse_url(url)
        record = Url.select().where(Url.url == url)
        if len(record):
            record = record.get()
            record.priority = priority
            record.language = language
            record.updated = datetime.now()
            record.referer = referer
            record.save()
            print('{} entry updated.'.format(url))
        else:
            Url.create(
                url=url,
                priority=priority,
                language=language,
                referer=referer,
                created=datetime.now(),
                updated=datetime.now(),
            )
            print('{} entry created.'.format(url))

    def parse_url(self, url):
        patterns = [
            (
                r'^https?://www.natureasia.com/{}/?$'.format(
                    self.languages_regex,
                ),
                1.0
            ),
            (
                r'^https?://www.natureasia.com/{}/[\w\-\.]+/?$'.format(
                    self.languages_regex,
                ),
                1.0,
            ),
            (
                r'^https?://www.natureasia.com/{}/[\w\-\.]+/toc/?$'.format(
                    self.languages_regex,
                ),
                1.0,
            ),
            (
                r'^https?://www.natureasia.com/{}/[\w\-\.]+/.+/?$'.format(
                    self.languages_regex,
                ),
                0.7,
            ),
        ]
        for pattern, priority in patterns:
            match = re.match(pattern, url)
            if match:
                return match.group(1), priority
        return '', 5.0


if __name__ == "__main__":
    # Create table if doesn't exist yet
    db.create_tables([Url])

    process = CrawlerProcess({
        'USER_AGENT': """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4)
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139
            Safari/537.36"""
    })

    process.crawl(MySpider)
    process.start()
