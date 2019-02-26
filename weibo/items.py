# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #support = scrapy.Field()
    #retweet = scrapy.Field()
    #comment = scrapy.Field()
    content = scrapy.Field()
    support_number = scrapy.Field()
    transpond_number = scrapy.Field()
    comment_number = scrapy.Field()
    date = scrapy.Field()

