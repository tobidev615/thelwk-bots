# -*- coding: utf-8 -*-
import scrapy


class HotelbotSpider(scrapy.Spider):
    name = 'hotelbot'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
