# encoding: utf-8

import scrapy
import time
from scrapy.http import Request
from weibo.items import WeiboItem   #新添加
from weibo.keywords import keyword
from scrapy.selector import Selector

class Weibo_Spider(scrapy.Spider):

    name = "weibo"
    #allowed_domains = ["weibo.cn/"]
    start_urls = [
            'https://s.weibo.com/article'
    ]

    def start_requests(self):
        for key_word in keyword:
            url = 'https://s.weibo.com/article?q=' + key_word
            yield Request(url, callback=self.parse_page, meta={'art': '文章', 'keyword': key_word}, dont_filter=True)

    def parse_page(self, response):
        item = WeiboItem()  # 新添加
        selector = Selector(response)
        article = selector.xpath("//div[@class='card-wrap']")
        for i in range(len(article)):

            item['article_news'] = response.meta['art']
            item['keyword'] = response.meta['keyword']
            item['title'] = article[i].xpath('//h3/a/text()').extract()[0]
            item['content'] = article[i].xpath('//h3/a/@href').extract()[0]
            #item['platform'] = article[i].xpath('//div]')[0].xpath('/a')[0].xpath('text()').extract()[0]
            #item['date'] = article[i].xpath('//div[@class="act"]/div/span')[1].xpath('text()').extract()[0]
            s_info = article[i].xpath('//div[@class="act"]/ul[@class="s-fr"]/li')
            #item['share_number'] = s_info[1].xpath('/a/text()').extract()[0]
            #if len(s_info) == 1:
            #    item['support_number'] = '0'
            #else:
            #    item['support_number'] = s_info[0].xpath('/a/text()').extract()[0]
            yield item



