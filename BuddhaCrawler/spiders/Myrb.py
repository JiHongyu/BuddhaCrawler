# -*- coding: utf-8 -*-

import time
import sys
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst

from BuddhaCrawler.items import BuddhacrawlerItem

sys.path.append("../")


class MyrbSpider(scrapy.Spider):
    name = 'myrb'
    protocol = 'http'
    host = 'www.myrb.net'
    city = '绵阳'
    allowed_domains = [host]
    start_urls = ['http://www.myrb.net/']

    def parse(self, response: scrapy.http.Response):

        yield self.collectDetailInfo(response)
        time.sleep(0.1)

        for urlXpath in response.xpath('//a/@href'):
            url = urlXpath.get()
            if url.startswith("/"):
                url = self.protocol + '://' + self.host + url
            if url is not None and url.find('javascript') < 0 and not url.startswith('#'):
                yield scrapy.Request(url=url, callback=self.parse)

    def collectDetailInfo(self, response: scrapy.http.Response):
        loader = ItemLoader(item=BuddhacrawlerItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('hostUrl', self.host)
        loader.add_value('city', self.city)
        loader.add_xpath('articleTitle',
                         "/html/body/center/div[@class='inner_page_2']/div[@class='inner_page_4']/div[@class='inner_page_138']/div[@class='inner_page_148']/text()")
        loader.add_xpath('articleText',
                         "/html/body/center/div[@class='inner_page_2']/div[@class='inner_page_4']/div[@class='inner_page_140']")
        loader.add_xpath('publishTime',
                         "/html/body/center/div[@class='inner_page_2']/div[@class='inner_page_4']/div[@class='inner_page_21']/text()")
        loader.add_value('coverPictureUrl', '')
        loader.add_value('articlePictureUrls', [])
        loader.add_value('articleVideoUrls', [])
        loader.add_value('createTime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return loader.load_item()
