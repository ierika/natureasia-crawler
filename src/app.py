import os
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from unipath import Path


class MySpider(CrawlSpider):
    name = 'natureasia.com'
    allowed_domains = ['natureasia.com', 'www.natureasia.com']
    start_urls = ['https://www.natureasia.com']
    url_set = set()
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Erase current file if it exists
        if self.export_file.exists():
            self.export_file.remove()
            self.export_file.write_file('')

    @property
    def export_file(self):
        return Path('{}/Downloads/natureasia_urls.txt'.format(
            os.getenv('HOME'),
        ))

    def parse_item(self, response):
        # url = response.url
        # if url.startswith('http://'):
        #     url = url.replace('http://', 'https://')
        # if url not in self.url_set:
        #     self.url_set.append(url)
        #     self.export_file.write_file('{}\n'.format(url), 'a')
        print(response.url)
        self.url_set.add(response.url)
