# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

class BuddhacrawlerItem(scrapy.Item):
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    hostUrl = scrapy.Field(
        output_processor=TakeFirst()
    )
    city = scrapy.Field(
        output_processor=TakeFirst()
    )
    articleTitle = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    articleTag = scrapy.Field(
        output_processor=Join(';')
    )
    articleText = scrapy.Field(
        output_processor=TakeFirst()
    )
    publishTime = scrapy.Field(
        output_processor=TakeFirst()
    )
    coverPictureUrl = scrapy.Field(
        output_processor=TakeFirst()
    )
    articlePictureUrls = scrapy.Field()
    articleVideoUrls = scrapy.Field()
    createTime = scrapy.Field(
        output_processor=TakeFirst()
    )
