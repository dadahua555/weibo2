# encoding: utf-8

import scrapy
import datetime
from weibo.bloomfilter import BloomFilter
from scrapy.http import Request
from weibo.items import WeiboItem
from weibo.keywords import keyword
from scrapy.selector import Selector
import sys
import io



reload(sys)
sys.setdefaultencoding('utf8')


bf = BloomFilter()
f = io.open('redundance.txt', 'w', encoding='utf-8')


class Weibo_Spider(scrapy.Spider):

    name = "weibo"
    #allowed_domains = ["weibo.cn/"]
    start_urls = [
            'https://s.weibo.com/article'
    ]

    def start_requests(self):

        for key_word in keyword:
            url = 'https://s.weibo.com/article?q=' + key_word
            yield Request(url, callback=self.parse, meta={'art': '文章', 'keyword': key_word}, dont_filter=True)

    def parse(self, response):
        selector = Selector(response)
        articles = selector.xpath("//div[@class='card-wrap']")
        for i in range(len(articles)-1):
            item = WeiboItem()  # 新添加
            item['article_news'] = response.meta['art']
            item['keyword'] = response.meta['keyword']
            flag_fault = 0

            try:
                item['title'] = articles[i].xpath('.//h3/a/@title').extract()[0]

                item['content'] = articles[i].xpath('.//h3/a/@href').extract()[0]
            except:
                print "@@@@@@@@出错啦啦啦啦啦啦！！！！"
                item['title'] = u''
                item['content'] = u''                     #　反正不会保存的，　免得去重的时候报错
                flag_fault = 1                            # 出错说明出现了无搜索结果的情况，刷新一下就好，但是这一次请求结果不保存
                yield Request(response.url, callback=self.parse,
                              meta={'art': '文章', 'keyword': response.meta['keyword']}, dont_filter=True)

            '''
            # 处理文章来源信息，有可能文章来源于微博账号，也可能来源于网址，两种处理
            try:
                item['platform'] = articles[i].xpath('.//div[@class="act"]/div/span')[0].xpath('./a')[0]\
                    .xpath('./text()').extract()[0]
            except:
                platform = articles[i].xpath('.//div[@class="act"]/div/span')[0].xpath('text()').extract()
                if len(platform) != 0:
                    item['platform'] = platform[0]
                else:
                    item['platform'] = '0'
            '''

            try:
                platform = articles[i].xpath('.//div[@class="act"]/div/span')[0]
                if len(platform.xpath('./a')) == 0:
                    platform_ = platform.xpath('text()').extract()
                    if len(platform_) != 0:
                        item['platform'] = platform_[0]
                    else:
                        item['platform'] = '0'
                else:
                    item['platform'] = platform.xpath('./a')[0].xpath('./text()').extract()[0]
            except:
                item['platform'] = u''

            try:
                # 时间处理
                list_ = articles[i].xpath('.//div[@class="act"]/div/span')[1].xpath('text()').extract_first().split()
                # 类似‘今天11:41’
                if list_[0][0] == u'今':
                    _time_ = list_[0].split('今天')[1].split(':')
                    date = datetime.datetime.now().strftime('%Y年%m月%d日') + _time_[0] + '时' + _time_[1] + '分'
                    item['date'] = date
                # 类似‘30分钟前’
                elif list_[0][-1] == u'前':
                    t = list_[0].split('分钟前')[0]
                    date = (datetime.datetime.now() - datetime.timedelta(minutes=int(t))).strftime("%Y年%m月%d日%H时%M分")
                    item['date'] = date
                # 类似‘02月27日 09:01’
                else:
                    _time_ = list_[1].split(':')
                    date = '2019年' + list_[0].decode('utf-8') + _time_[0] + '时' + _time_[1] + '分'
                    item['date'] = date
            except:
                item['date'] = datetime.datetime.now().strftime('%Y年%m月%d日%H时%M分')

            s_info = articles[i].xpath('.//div[@class="act"]/ul[@class="s-fr"]/li')

            try:
                # 分享数处理
                share = s_info[0].xpath('./a/text()').extract_first()
                share = share.split('分享')[1]
                if share == '':
                    item['share_number'] = '0'
                else:
                    item['share_number'] = share
            except:
                pass

            # 支持数处理，有些文章不能支持，要分别处理
            if len(s_info) == 1:
                item['support_number'] = '0'
            else:
                try:
                    item['support_number'] = s_info[1].xpath('.//span[@node-type="likeNum"]/text()').extract()[0]
                except:
                    item['support_number'] = '0'

            # url去重，已经爬过的文章不需要再存进数据库，把它的标题写进redundance.txt
            if bf.isContains(item['content'], "testurl"):
                line = item['title'] + '\n'
                f.write(line)

            else:
                try:
                    if flag_fault == 0:
                        bf.insert(item['content'], "testurl")
                        yield item
                except:
                    pass

        # 有下一页的话要继续爬，没有的话，直接退出
        try:
            next_href = selector.xpath('//div[@class="m-page"]/div/a[@class="next"]/@href').extract()[0]
            url = 'https://s.weibo.com' + next_href
            print response.request.headers['User-Agent']
            yield Request(url, callback=self.parse,
                          meta={'art': '文章', 'keyword': response.meta['keyword']}, dont_filter=True)
        except:
            print "没有下一页"






