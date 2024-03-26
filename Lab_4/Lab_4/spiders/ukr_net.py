import scrapy


class UkrNetSpider(scrapy.Spider):
    name = "ukr_net"
    allowed_domains = ["ukr.net"]
    start_urls = ["https://ukr.net"]

    def parse(self, response):
        pass
