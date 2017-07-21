# -*- coding: utf-8 -*-
import scrapy
from plantomjsTest.items import Jd2Item


class Jd2Spider(scrapy.Spider):
    name = 'jd_2'
    allowed_domains = ['jd.com']
    start_urls = [
        'https://search.jd.com/Search?keyword={key}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={key}&wtype=1&click=1'.format(key = '诸神的微笑 九州出版社')
        ]

    def parse(self, response):
        content = response.body.decode(encoding="utf-8", errors="strict")
        sel = scrapy.selector.Selector(text=content).xpath('//div[@id="J_goodsList"]')

        jd_good = Jd2Item()
        for good in sel.xpath('.//ul[@class="gl-warp clearfix"]/li[@class="gl-item"]'):
            jd_good['good_id'] = good.xpath('.//@data-sku').extract_first()
            jd_good['name'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-name"]/a/em/font/text()').extract()
            jd_good['commit'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-commit"]/strong/a/text()').extract_first()
            jd_good['price'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/@data-price').extract_first()
            jd_good['img'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-img"]/a/img/@src').extract_first()
            jd_good['detail_url'] = "https:{}#comment".format(good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-img"]/a/@href').extract_first())
            if(len(jd_good['name']) > 0):
                break

        for i in range(0, 30):
            tmp = jd_good
            yield scrapy.Request(url="https://sclub.jd.com/comment/productPageComments.action?productId={good_id}&score=0&sortType=3&page={page}&pageSize={pageSize}&isShadowSku=0&callback=fetch"
                        .format(good_id = tmp['good_id'], page = i, pageSize = 10)
                        , meta={'good':tmp},callback=self.parse_comment,dont_filter=True)            
            

    def parse_comment(self, response):
        good = Jd2Item()
        content = response.body.decode(encoding="utf-8", errors="strict")
        body = scrapy.selector.Selector(text=content).xpath('//body')
        tmp = response.meta['good']
        good['comments'] = body.extract()
        good['good_id'] = tmp['good_id']
        good['name'] = tmp['name']
        good['commit'] = tmp['commit']
        good['price'] = tmp['price']
        good['img'] = tmp['img']
        good['detail_url'] = tmp['detail_url']
        yield good
