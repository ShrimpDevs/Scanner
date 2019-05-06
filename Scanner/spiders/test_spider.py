# -*- coding: utf-8 -*-
import scrapy


class TestSpiderSpider(scrapy.Spider):
    name = 'test_spider'
    allowed_domains = ['http://pycoder.ru/?page=1']
    start_urls = ['http://http://pycoder.ru/?page=1/']

    def parse(self, response):
        pass
