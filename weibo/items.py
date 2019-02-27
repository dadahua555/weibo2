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
    article_news = scrapy.Field()
    platform = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    support_number = scrapy.Field()
    share_number = scrapy.Field()
    keyword = scrapy.Field()



