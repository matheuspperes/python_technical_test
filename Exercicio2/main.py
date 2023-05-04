from scrapy.crawler import CrawlerProcess
from myspider import MySpider


def start():
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    return

start()