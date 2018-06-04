import os
import re
from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from unipath import Path

import models


class MySpider(CrawlSpider):
    """
    Crawls the entire NatureAsia.com.
    Excludes 'zh-tw' website though.
    """
    name = 'natureasia.com'
    allowed_domains = ['natureasia.com', 'www.natureasia.com']
    root_url = 'https://www.natureasia.com'
    rules = (
        Rule(
            LinkExtractor(
                allow=r'https?://www\.natureasia\.com/(ja-jp|ko-kr|en)',
                deny=[
                    r'https?://www\.natureasia\.com/en/(middleeast|nindia)',
                    r'https?://www\.natureasia\.com/secure/.*',
                ],
                allow_domains=allowed_domains,
            ),
            callback='parse_item',
            follow=True,
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define start URLs
        self.start_urls = [
            self.root_url + '/ja-jp',
            self.root_url + '/en',
            self.root_url + '/ko-kr',
        ]

    @property
    def export_file(self):
        """
        Return a Path object of the output file.
        The output file will contain the URLs that was crawled.
        """
        return Path('{}/Downloads/sitemap_{}.xml'.format(
            os.getenv('HOME'),
            datetime.now().strftime('')
        ))

    def parse_item(self, response):
        """
        Update or create database entry.

        If the URL already exist in the database,
        update the priority instead just in case it changed.
        Otherwise, just create an entry.
        """
        if response.url.startswith('https'):
            language, priority = self.parse_url(response.url)
            try:
                url = models.Url.get(url=response.url)
                url.priority = priority
                url.language = language
                url.update = datetime.now()
                url.save()
                print('{} entry updated.'.format(response.url))
            except Exception as e:
                models.Url.create(
                    url=response.url,
                    priority=priority,
                    language=language,
                )
                print('{} entry created.'.format(response.url))

    def parse_url(self, url):
        patterns = [
            (r'^https?://www.natureasia.com/(ja-jp|zh-tw|en)/?$', 1.0),
            (r'^https?://www.natureasia.com/(ja-jp|zh-tw|en)/[\w\-\.]+/?$', 1.0),
            (r'^https?://www.natureasia.com/(ja-jp|zh-tw|en)/[\w\-\.]+/toc/?$', 1.0),
            (r'^https?://www.natureasia.com/(ja-jp|zh-tw|en)/[\w\-\.]+/.+/?$', 0.7),
        ]
        for pattern, priority in patterns:
            match = re.match(pattern, url)
            if match:
                return match.group(1), priority
        return '', 5.0


if __name__ == "__main__":
    # Create table if doesn't exist yet
    models.db.create_tables([models.Url])

    process = CrawlerProcess({
        'USER_AGENT': """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4)
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139
            Safari/537.36"""
    })

    process.crawl(MySpider)
    process.start()
