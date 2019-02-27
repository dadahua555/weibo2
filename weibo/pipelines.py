# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import io
import json
import pymongo
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class WeiboPipeline(object):
    def __init__(self):
        self.f = io.open('result.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, encoding='utf-8') + '\n'
        self.f.write(line)
        return item

    def close_spider(self, spider):
        self.f.close()



class FilePipeline(object):
    def process_item(self, item, spider):
        with io.open('cnblog.txt', 'w', encoding='utf-8') as f:
            #titles = item['title']
            #links = item['link']
            contents = item['content']
            for i in contents:
                f.write(i + '\n')
        return item


class MongoPipeline(object):
    collection = 'article'  #mongo数据库的collection名字，随便

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):                  #爬虫一旦开启，就会实现这个方法，连接到数据库
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):            #爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        self.client.close()

    def process_item(self, item, spider):  
        '''
        每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''
        #line = json.dumps(dict(item), encoding='utf-8')
        table = self.db[self.collection]
        table.insert(dict(item))
        return item
