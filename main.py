from scrapy.crawler import CrawlerProcess

from src.models import db
from src.models import Url
from src.crawler import MySpider


if __name__ == "__main__":
    # Create table if doesn't exist yet
    db.create_tables([Url])

    # Begin crawl process
    process = CrawlerProcess({
        'USER_AGENT': """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4)
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139
            Safari/537.36"""
    })
    process.crawl(MySpider)
    process.start()
