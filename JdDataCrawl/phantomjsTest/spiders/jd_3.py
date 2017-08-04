# -*- coding: utf-8 -*-

""" module docstring """
import json
import scrapy
from plantomjsTest.items import Jd2Item

# 标识递归是否第一次进入
# enter = 0

class Jd3Spider(scrapy.Spider):
    """ class docstring """
    name = 'jd_3'
    allowed_domains = ['jd.com']
    start_urls = ['http://ip:port/solr/xxzx_sales/select?q=*:*&wt=json&indent=true&rows=0&json.facet={{fz:{{type:terms,field:isbn,sort:"sumcnt desc",offset:0,limit:100,facet:{{sumcnt:"sum(cnt)",bookname:{{type:terms,field:bookname}},press:{{type:terms,field:press}}}}}}}}&fq=year:2017&fq=press:{press}'.format(press = '百花洲文艺出版社有限责任公司')]
    # 百花洲文艺出版社有限责任公司
    # 湖南岳麓书社
    def parse(self, response):
        # global enter
        html = response.body.decode(encoding="utf-8", errors="strict")
        solr_json = scrapy.selector.Selector(text=html).xpath('//body/pre/text()').extract_first()

        books = json.loads(solr_json)

        for book in books['facets']['fz']['buckets']:
            isbn = book['val']
            bookname = book['bookname']['buckets'][0]['val']
            press = '百花洲文艺出版社' #book['press']['buckets'][0]['val']

            with open('book.txt','a',encoding='utf-8') as writer:
                writer.write('{} {}\r\n'.format(bookname, press))

            yield scrapy.Request(url='https://search.jd.com/Search?keyword={key}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={key}&wtype=1&click=1'.format(key = bookname + ' ' + press), callback=self.parse_jd, dont_filter=True, meta={'book':bookname,'press':press,'isbn':isbn})

        # press_lst = ['化学工业出版社', '中国建筑工业出版社', '湖南文艺出版社', '二十一世纪出版社', '人民邮电出版社']
        
        # for press in press_lst:
        #     if press == '化学工业出版社':
        #         enter += 1
        #     if enter <= 1:
        #         yield scrapy.Request(url='http://ip:port/solr/xxzx_sales/select?q=*:*&wt=json&indent=true&rows=0&json.facet={{fz:{{type:terms,field:isbn,sort:"sumcnt desc",offset:0,limit:100,facet:{{sumcnt:"sum(cnt)",bookname:{{type:terms,field:bookname}},press:{{type:terms,field:press}}}}}}}}&fq=year:2017&fq=press:{press}'.format(press = press), callback=self.parse, dont_filter=True)
        #     else:
        #         break

    def parse_jd(self, response):
        content = response.body.decode(encoding="utf-8", errors="strict")
        sel = scrapy.selector.Selector(text=content).xpath('//div[@id="J_goodsList"]')
        isbn = response.meta['isbn']
        book = response.meta['book']

        jd_good = Jd2Item()
        try:
            for good in sel.xpath('.//ul[@class="gl-warp clearfix"]/li[@class="gl-item"]'):
                jd_good['good_id'] = good.xpath('.//@data-sku').extract_first()
                jd_good['name'] = book
                jd_good['commit'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-commit"]/strong/a/text()').extract_first()
                jd_good['price'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/@data-price').extract_first()
                jd_good['img'] = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-img"]/a/img/@src').extract_first()
                jd_good['detail_url'] = "https:{}#comment".format(good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-img"]/a/@href').extract_first())
                jd_good['isbn'] = isbn

                # 查询结果关键字（红色字体）如果存在就使用该商品id。解决查询时出现前几个结果与关键字无关的关联查询。
                key_name = good.xpath('.//div[@class="gl-i-wrap"]/div[@class="p-name"]/a/em/font/text()').extract()
                if(len(key_name) > 0):
                    break
            
            # 京东最多允许查询1000条评论 
            # 获取评论页码
            page = 1
            if '万' in jd_good['commit']:
                page = 100
            elif '+' in jd_good['commit']:
                commit = int(jd_good['commit'].replace('+',''))
                init = int(commit/10)
                offset = 1 if init < 10 else 10
                page = init + offset
                page = page if page < 100 else 100
            else:
                page = 1

            with open('page.txt', 'a', encoding='utf-8') as p:
                p.write('book:{},page:{}\r\n'.format(book,page))

            for i in range(0, page):
                tmp = jd_good
                yield scrapy.Request(url="https://sclub.jd.com/comment/productPageComments.action?productId={good_id}&score=0&sortType=3&page={page}&pageSize={pageSize}&isShadowSku=0&callback=fetch"
                            .format(good_id = tmp['good_id'], page = i, pageSize = 10)
                            , meta={'good':tmp},callback=self.parse_comment,dont_filter=True)
                            
        except KeyError as e:
            log = open('error.txt', 'a', encoding='utf-8')
            log.write('key error:{}\r\n'.format(e))
            log.close()

        
    def parse_comment(self, response):
        good = Jd2Item()
        content = response.body.decode(encoding="utf-8", errors="strict")
        body = scrapy.selector.Selector(text=content).xpath('//body')
        tmp = response.meta['good']
        good['comments'] = body.extract_first()
        good['good_id'] = tmp['good_id']
        good['name'] = tmp['name']
        good['commit'] = tmp['commit']
        good['price'] = tmp['price']
        good['img'] = tmp['img']
        good['detail_url'] = tmp['detail_url']
        good['isbn'] = tmp['isbn']

        if len(good['comments']) > 900:
            yield good

