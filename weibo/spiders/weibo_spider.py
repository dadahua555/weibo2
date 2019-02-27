# encoding: utf-8

import scrapy
import time
import json
import random
from scrapy.http import Request
from weibo.items import WeiboItem   #新添加
from weibo.keywords import keyword
from weibo.cookies import cookies
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
            yield Request(url, callback=self.parse, meta={'art': '文章', 'keyword': key_word})

    def parse(self, response):
        cookie = json.loads(random.choice(cookies))
        selector = Selector(response)
        articles = selector.xpath("//div[@class='card-wrap']")
        for i in range(len(articles)-1):
            item = WeiboItem()  # 新添加
            item['article_news'] = response.meta['art']
            item['keyword'] = response.meta['keyword']
            item['title'] = articles[i].xpath('.//h3/a/@title').extract()[0]
            item['content'] = articles[i].xpath('.//h3/a/@href').extract()[0]
            try:
                item['platform'] = articles[i].xpath('.//div[@class="act"]/div/span')[0].xpath('./a')[0]\
                    .xpath('./text()').extract()[0]
            except:
                item['platform'] = articles[i].xpath('.//div[@class="act"]/div/span')[0].xpath('text()').extract()
            item['date'] = articles[i].xpath('.//div[@class="act"]/div/span')[1].xpath('text()').extract()[0]
            s_info = articles[i].xpath('.//div[@class="act"]/ul[@class="s-fr"]/li')
            item['share_number'] = s_info[0].xpath('./a/text()').extract()[0]
            if len(s_info) == 1:
                item['support_number'] = '0'
            else:
                try:
                    item['support_number'] = s_info[1].xpath('.//span[@node-type="likeNum"]/text()').extract()[0]
                except:
                    item['support_number'] = '0'
            yield item
        '''
        try:
            next_href = selector.xpath('//*[@class="next"]/@href').extract()[0]
            print next_href
            yield Request('https://s.weibo.com' + next_href, callback=self.parse, cookies=cookie,
                          meta={'art': '文章', 'keyword': response.meta['keyword']})
        except:
            pass
        '''






