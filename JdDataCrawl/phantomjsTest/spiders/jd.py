# -*- coding: utf-8 -*-
import scrapy
from plantomjsTest.items import JdItem

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = [
        'https://search.jd.com/Search?keyword={key}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={key}&wtype=1&click=1'.format(key = '平凡的世界')
        # 'https://item.jd.com/11736013.html?dist=jd'
        ]

    def parse(self, response):
        detail_url = ""; # 因为相同关键字搜索的多个商品下的评论基本上一致，所以只取一个商品评价就好了
        content = response.body.decode(encoding="utf-8", errors="strict")
        sel = scrapy.selector.Selector(text=content).xpath('//div[@id="J_goodsList"]')

        jd_good = JdItem()
        for good in sel.xpath('.//ul[@class="gl-warp clearfix"]/li[@class="gl-item"]'):
            jd_good['good_id'] = good.xpath('.//@data-sku').extract_first()
            jd_good['name'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-name"]/a/em/font/text()').extract()
            jd_good['commit'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-commit"]/strong/a/text()').extract_first()
            jd_good['price'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/@data-price').extract_first()
            jd_good['img'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-img"]/a/img/@src').extract_first()
            jd_good['detail_url'] = "https:{}#comment".format(good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-img"]/a/@href').extract_first())
            if(len(jd_good['name']) > 0):
                detail_url = jd_good['detail_url']
                break

        yield scrapy.Request(url=detail_url, meta={'good':jd_good},callback=self.parse_comment,dont_filter=True)
            

    def parse_comment(self, response):
        content = response.body.decode(encoding="utf-8", errors="strict")
        sel = scrapy.selector.Selector(text=content).xpath('//div[@id="comment-0"]')

        good = response.meta['good']
        for comment in sel.xpath('.//div[@class="comments-item"]/div[@class="com-item-main clearfix"]'):
            tmp = good
            tmp['user'] = comment.xpath('.//div[@class="column column3"]/div/div[@class="user-name"]/text()').extract()
            tmp['kind'] = comment.xpath('.//div[@class="column column1"]/div[@class="features type-item"]/ul/li/text()').extract_first()
            tmp['status'] = comment.xpath('.//div[@class="column column2"]/div[@class="p-comment"]/text()').extract_first()
            tmp['star'] = comment.xpath('.//div[@class="column column1"]/div[1]/@class').extract()
            tmp['created_at'] = comment.xpath('.//div[@class="column column1"]/div[@class="comment-time type-item"]/text()').extract()
            tmp['device'] = comment.xpath('.//div[@class="column column3"]/div[@class="user-item"]/span[@class="user-access"]/text()').extract_first()
            tmp['level'] = comment.xpath('.//div[@class="column column3"]/div[@class="type-item"]/span[@class="u-vip-level"]/text()').extract_first()
            tmp['url'] = comment.xpath('.//div[@class="column column2"]/div[@class="comment-operate"]/a[@class="replylz J-reply-trigger"]/@href').extract_first()
            tmp['comments_count'] = comment.xpath('.//div[@class="column column2"]/div[@class="comment-operate"]/a[@class="replylz J-reply-trigger"]/span/text()').extract_first()
            tmp['attitudes_count'] = comment.xpath('.//div[@class="column column2"]/div[@class="comment-operate"]/a[@class="nice J-nice"]/@title').extract_first()
            yield tmp

        next_page = sel.xpath('//a[@class="ui-pager-next"]').extract_first()
        if next_page :
            pass
