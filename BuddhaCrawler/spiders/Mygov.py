# -*- coding: utf-8 -*-

import time
import sys
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst

from BuddhaCrawler.items import BuddhacrawlerItem

sys.path.append("../")


class MygovSpider(scrapy.Spider):
    name = 'mygov'
    protocol = 'http'
    host = 'my.gov.cn'
    city = '绵阳'
    allowed_domains = [host]
    start_urls = ['http://www.my.gov.cn/']

    def parse(self, response: scrapy.http.Response):

        raw_item = self.collectDetailInfo(response)
        MygovSpider.processItem(raw_item)
        yield raw_item

        time.sleep(0.1)

        for urlXpath in response.xpath('//a/@href'):
            url = urlXpath.get()
            if url.startswith("/"):
                url = self.protocol + '://' + self.host + url
            if url is not None and url.find('javascript') < 0 and not url.startswith('#'):
                yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def processItem(cls, item: BuddhacrawlerItem):

        publishTime = item.get('publishTime')
        if publishTime is not None:
            try:
                publishTime = datetime.strptime(publishTime, '%Y-%m-%d %H:%M')
                item['publishTime'] = publishTime.strftime('%Y-%m-%d %H:%M:%S')
            except:
                item['publishTime'] = None
        return item

    def collectDetailInfo(self, response: scrapy.http.Response):
        loader = ItemLoader(item=BuddhacrawlerItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('hostUrl', self.host)
        loader.add_value('city', self.city)
        loader.add_xpath('articleTitle',
                         "/html/body/div[@id='container']/div[@class='container']/div[@class='wz_contain']/div[@class='con_main']/h1[@class='newstitle']/text()")
        loader.add_xpath('articleText',
                         "/html/body/div[@id='container']/div[@class='container']/div[@class='wz_contain']/div[@class='con_main']/div[@id='zoom']")
        loader.add_xpath('publishTime',
                         "/html/body/div[@id='container']/div[@class='container']/div[@class='wz_contain']/div[@class='con_main']/div[@class='newsinfo']/div[@class='fl newsinfoleft']/span/text()")
        loader.add_value('coverPictureUrl', '')
        loader.add_value('articlePictureUrls', [])
        loader.add_value('articleVideoUrls', [])
        loader.add_value('createTime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return loader.load_item()
