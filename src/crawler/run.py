# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from crawler.yahoo_finance.spiders.yahoo_finance_spider import YahooFinanceSpider


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(YahooFinanceSpider)
process.start() # the script will block here until the crawling is finished
