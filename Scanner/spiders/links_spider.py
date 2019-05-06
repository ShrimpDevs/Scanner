# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor

class LinksSpiderSpider(scrapy.Spider):
    name = 'links_spider' # scrapy crawl links_spider - run spider
    #allowed_domains = ['http://check.std-320.ist.mospolytech.ru/']
    start_urls = ['http://check.std-320.ist.mospolytech.ru/']

    collected_urls = []

    def toLogFile(self, text):
        f = open('C:\\Users\\alexp\\Desktop\\test.txt','a')
        f.write(text + '\n')
        f.close()

    def parse(self, response):
        le = LinkExtractor()
        #self.toLogFile('start parse')
        self.logger.info('start parse')
        for link in le.extract_links(response):
            self.collected_urls.append(link.url)
            self.toLogFile('')
            if link.url == 'something I want':
                pass

        #self.toLogFile('all links(',self.collected_urls.count(),'):')
        for line in self.collected_urls:
            self.logger.info(line)
        #    self.toLogFile(line)
