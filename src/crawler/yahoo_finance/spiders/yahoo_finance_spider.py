# -*- coding: utf-8 -*-

import os
import scrapy
from settings import DATA_RAW_HTML_DIR


class YahooFinanceSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = os.path.join(DATA_RAW_HTML_DIR, 'quotes-%s.html' % page)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
