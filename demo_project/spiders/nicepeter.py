import scrapy
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random, logging

class NicepeterSpider(scrapy.Spider):
    #identity
    name="nicepeter"

    #Request
    def start_requests(self):
        urls= [
            'https://www.redfin.com'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    #Response
    def parse(self, response):
        _file= "{0}.html".format(13)

        with open(_file, "wb") as f:
            f.write(response.body)