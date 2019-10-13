# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from BuddhaCrawler.DBUtil import dbUtil
from BuddhaCrawler.DBUtil import CollectWebInfo
from scrapy.exceptions import DropItem


class NormalHtmlPipeline(object):
    def process_item(self, item, spider):
        print('--------------------------')
        if item.get('articleTitle', '').strip() == '' or item.get('articleText', '').strip() == '':
            raise DropItem('无实际意义数据')
        return item


class DBPipeline(object):
    count = 0

    def process_item(self, item, spider):
        dbUtil.getSession()
        keys = item.keys()
        collectionWebInfo = CollectWebInfo()
        for key, value in item.items():
            setattr(collectionWebInfo, key, value)

        session = dbUtil.getSession()
        session.add(collectionWebInfo)

        session.commit()
        self.count += 1
        print('WRITE DB SUCCESS')

        return item
