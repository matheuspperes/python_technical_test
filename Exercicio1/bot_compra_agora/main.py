from scrapy.crawler import CrawlerProcess
from bot_start import MySpider

def start():
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    return

start()