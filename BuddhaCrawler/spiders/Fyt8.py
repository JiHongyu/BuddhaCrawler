# -*- coding: utf-8 -*-

import time
import sys
import traceback
from datetime import datetime
from urllib.parse import urlparse
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst

from BuddhaCrawler.items import BuddhacrawlerItem

sys.path.append("../")

dateYYmmddHHmm_r = re.compile('([0-9]{1,2})月([0-9]{1,2})日')


class Fyt8Spider(scrapy.Spider):
    name = 'fyt8'
    allowed_domains = ['www.fyt8.cn']
    start_urls = ['https://www.fyt8.cn']
    protocol = 'https'
    host = 'www.fyt8.cn'
    city = '阜阳'

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
            res = dateYYmmddHHmm_r.search(publishTime)
            if res is not None and res.group(0) is not None:
                p = datetime(datetime.now().year, int(res.group(1)), int(res.group(2)))
                item['publishTime'] = p.strftime('%Y-%m-%d %H:%M:%S')
            else:
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
                         "//div[@class='newsBox']/div[@class='bt']/h2[@class='bt1']/text()")
        loader.add_xpath('articleTag',
                         "//div[@class='newslink']/a/text()")
        loader.add_xpath('articleText',
                         "//div[@class='newsBox']/div[@class='newsCon']")
        loader.add_xpath('publishTime',
                         "//div[@class='newsBox']/div[@class='bt']/div[@class='bt2']/text()")
        loader.add_value('coverPictureUrl', '')
        loader.add_xpath('articlePictureUrls',
                         "//div[@class='newsBox']/div[@class='newsCon']/div[@class='pgc-img']/img/@src")
        loader.add_value('articleVideoUrls', [])
        loader.add_value('createTime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return loader.load_item()
