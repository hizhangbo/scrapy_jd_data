# -*- coding: utf-8 -*-
from urllib import parse
import scrapy
import scrapy.selector
from plantomjsTest.items import WeiboItem

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['s.weibo.com']
    start_urls = ["http://s.weibo.com/weibo/{}&nodup=1".format(parse.quote_plus(parse.quote_plus('诸神的微笑 九州出版社')))]

    def parse(self, response):
        content = response.body.decode(encoding="utf-8", errors="strict")
        sel = scrapy.selector.Selector(text=content).xpath('//div[@class="S_plwrap"]')
        # 写入文件
        # filename = 'weibo.txt'
        # with open(filename, 'w+', encoding='utf-8') as f:
        #     f.write(sel.extract()[0])
        # print('写入成功！！！')

        # 微博元素对象化
        wbconList = []
        # idx = 0
        for p in sel.xpath('.//div[@action-type="feed_list_item"]'):
            weibo_text = p.extract()
            # idx += 1
            # with open('weibo_'+ str(idx), 'w+', encoding='utf-8') as f:
            #     f.write(weibo_text)

            sel = scrapy.selector.Selector(text=weibo_text)

            item = WeiboItem()
            item['user'] = str(p.xpath('.//p[@class="comment_txt"]/@nick-name').extract())
            item['status'] = str(p.xpath('.//p[@class="comment_txt"]/text()').extract())
            item['created_at'] = str(p.xpath('.//a[@class="W_textb"]/@title').extract())
            item['device'] = str(p.xpath('.//a[@rel]/text()').extract())
            item['reposts_count'] = str(p.xpath('.//span[contains(./text(),"转发")]/em/text()').extract())
            item['comments_count'] = str(p.xpath('.//span[contains(./text(),"评论")]/em/text()').extract())
            item['attitudes_count'] = str(p.xpath('.//a[@title="赞"]/span/em/text()').extract())
            item['search_text'] = str(p.xpath('//div[@class="search_head_formbox"]/div/div/div/div/input[@class="searchInp_form"][1]/@value').extract())
            item['url'] = str(p.xpath('.//a[@class="W_textb"]/@href').extract())
            wbconList.append(item)
        
        return wbconList
