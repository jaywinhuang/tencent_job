# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentJobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    duty = scrapy.Field()
    requirement = scrapy.Field()
    location = scrapy.Field()
    category = scrapy.Field()
    issue_time = scrapy.Field()
    link = scrapy.Field()
