# encoding: utf-8

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from weibo.items import WeiboItem   #新添加

class Weibo_Spider(scrapy.Spider):

    name = "weibo"
    #allowed_domains = ["weibo.cn/"]
    start_urls = [
            'https://weibo.cn/midea'
    ]
    def start_requests(self):
        yield Request('https://weibo.cn/mideabingxiang', cookies={"SCF": "Aksmea4EpLAdD2xfueYpin7kakm0e8nDiUVPl5i7VzU9LMVIFvi9FyL3Xh4t7xHm4cR0xBSeQtlpwLQgzBZKsCo.", "SSOLoginState": "1551150521", "SUB": "_2A25xcN3pDeRhGeRJ6lQS9yzFyj2IHXVSmuOhrDV6PUJbkdANLVD4kW1NUnmjmxepssTwVKyxtdKj5Wc4jBpHzms_", "SUHB": "0id60pWmsuOZ8g"}, callback=self.parse)


    def parse(self, response):
        #item = WeiboItem()    #新添加
        #item['content'] = response.xpath('//span[@class="ctt"]/text()').extract()
        #yield item
        weibo_item = WeiboItem()
        selector = Selector(response)
        wbs = selector.xpath("//div[@class='c']") # get all elements which class name is 'c'
        for i in range(len(wbs) - 2):
            divs = wbs[i].xpath('./div')
            weibo_item['content'] = divs[0].xpath('./span[@class="ctt"]/text()').extract()
            if len(divs) == 1:
                a = divs[0].xpath('./a')
                if len(a) > 0:
                    for j in range(len(a)):
                        weibo_item['support_number'] = a[-4].xpath('./text()').extract()
                        weibo_item['transpond_number'] = a[-3].xpath('./text()').extract()
                        weibo_item['comment_number'] = a[-2].xpath('./text()').extract()
                weibo_item['date'] = divs[0].xpath('./span[@class="ct"]/text()').extract()
            if len(divs) == 2:
                a = divs[1].xpath('./a')
                if len(a) > 0:
                    for j in range(len(a)):
                        weibo_item['support_number'] = a[-4].xpath('./text()').extract()
                        weibo_item['transpond_number'] = a[-3].xpath('./text()').extract()
                        weibo_item['comment_number'] = a[-2].xpath('./text()').extract()
                weibo_item['date'] = divs[1].xpath('./span[@class="ct"]/text()').extract()
            yield weibo_item
#        if selector.xpath('//*[@id="pagelist"]/form/div/a/text()').extract()[0] == u'下页':
#            next_href = selector.xpath('//*[@id="pagelist"]/form/div/a/@href').extract()[0]
#            yield Request('https://weibo.cn' + next_href, callback=self.parse)
