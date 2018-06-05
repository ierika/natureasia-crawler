import re
from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from xml_exporter import Xml
from models import db
from models import Url


"""
The fastest way to bulk insert data into the database

It's not currently implement because of my limited knowledge of Scrapy,
but I hope it will be soon. This is here so I will be reminded.

http://docs.peewee-orm.com/en/latest/peewee/querying.html#bulk-inserts
"""


class MySpider(CrawlSpider):
    """
    Crawls the entire NatureAsia.com.
    Excludes 'zh-tw' website though.
    """
    name = 'natureasia.com'
    allowed_domains = ['natureasia.com']
    start_urls = ['https://www.natureasia.com']
    languages_regex = r'(ja-jp|en|ko-kr)'
    rules = (
        Rule(
            LinkExtractor(
                allow=r'natureasia\.com',
                deny=(
                    r'natureasia\.com/en/(nmiddleeast|nindia)',
                    r'natureasia\.com/(zh-tw|zh-cn)',
                    r'natureasia\.com/secure',
                ),
            ),
            callback='parse_item',
            follow=True,
        ),
    )

    def start_requests(self):
        """
        If one of the start_urls has been crawled.
        Do not run them again.
        """
        for url in self.start_urls:
            yield Request(url)

    def parse_item(self, response):
        """
        Update or create database entry.

        If the URL already exist in the database,
        update the priority instead just in case it changed.
        Otherwise, just create an entry.
        """
        referer = response.request.headers.get('Referer', '')
        url = response.url.replace('http://', 'https://')
        url = url.rstrip('/')
        language, priority = self.parse_url(url)
        with db.atomic():
            record = Url.select().where(Url.url == url)
            current_datetime = datetime.now()
            if len(record):
                record = record.get()
                record.priority = priority
                record.language = language
                record.updated = current_datetime
                record.referer = referer
                record.save()
                print('{} entry updated.'.format(url))
            else:
                Url.create(
                    url=url,
                    priority=priority,
                    language=language,
                    referer=referer,
                    created=current_datetime,
                    updated=current_datetime,
                )
                print('{} entry created.'.format(url))

    def parse_url(self, url):
        """
        Set priority level from the specified patterns below,
        And extract language information.
        """
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

    def spider_closed(self):
        """Generate XML after everything is done"""
        Xml().generate_xml()
