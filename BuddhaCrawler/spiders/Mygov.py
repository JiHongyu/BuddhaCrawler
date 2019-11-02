# -*- coding: utf-8 -*-

import time
import sys
import traceback
from datetime import datetime
from urllib.parse import urlparse

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

        try:
            raw_item = self.collectDetailInfo(response)
            self.processItem(raw_item)
            yield raw_item
        except:
            print('-----------SPIDER_ERROR-----------')
            traceback.print_exc()

        time.sleep(0.1)

        for urlXpath in response.xpath('//a/@href'):
            url = urlXpath.get()
            if url.startswith("/"):
                url = self.protocol + '://' + self.host + url
            if url is not None and url.find('javascript') < 0 and not url.startswith('#'):
                try:
                    yield scrapy.Request(url=url, callback=self.parse)
                except:
                    traceback.print_exc()
                    pass

    @classmethod
    def processItem(cls, item: BuddhacrawlerItem):

        # 获取文章发布时间
        publishTime = item.get('publishTime')
        if publishTime is not None:
            try:
                publishTime = datetime.strptime(publishTime, '%Y-%m-%d %H:%M')
                item['publishTime'] = publishTime.strftime('%Y-%m-%d %H:%M:%S')
            except:
                item['publishTime'] = None




        if item.get('articlePictureUrls') is not None:
            cnt = 0
            imgUrlStrList = []
            for url in item.get('articlePictureUrls'):
                cnt += 1
                u = urlparse(item.get('url'))
                data = None

                if url.find(u.scheme) < 0:
                    data = 'img%s %s' % (cnt, u.scheme + '://' + u.hostname + url)
                else:
                    data = 'img%s %s' % (cnt, url)
                imgUrlStrList.append(data)
            item['articlePictureUrls'] = ';'.join(imgUrlStrList)

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
        loader.add_xpath('articlePictureUrls', "/html/body/div[@id='container']/div[@class='container']/div[@class='wz_contain']/div[@class='con_main']/div[@id='zoom']//img/@src")
        loader.add_value('articleVideoUrls', [])
        loader.add_value('createTime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return loader.load_item()
