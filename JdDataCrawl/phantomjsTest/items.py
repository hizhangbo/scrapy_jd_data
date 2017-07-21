# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    _id = scrapy.Field()             # id
    user = scrapy.Field()            # 微博发送者
    status = scrapy.Field()          # 微博内容
    created_at = scrapy.Field()      # 微博发送时间
    device = scrapy.Field()          # 发送设备
    reposts_count = scrapy.Field()   # 转发数
    comments_count = scrapy.Field()  # 评论数
    attitudes_count = scrapy.Field() # 点赞数
    search_text = scrapy.Field()     # 搜索文本
    url = scrapy.Field()             # 微博地址

class JdItem(scrapy.Item):
    _id = scrapy.Field()             # id
    good_id = scrapy.Field()         # 商品id
    name = scrapy.Field()            # 商品名称
    commit = scrapy.Field()          # 评价数
    price = scrapy.Field()           # 价格
    img = scrapy.Field()             # 商品图片
    detail_url = scrapy.Field()      # 详情页url
    user = scrapy.Field()            # 京东昵称
    kind = scrapy.Field()            # 商品套餐
    status = scrapy.Field()          # 购买评价
    star = scrapy.Field()            # 好评星级
    created_at = scrapy.Field()      # 发表时间
    device = scrapy.Field()          # 发送设备
    level = scrapy.Field()           # 用户等级
    url = scrapy.Field()             # 评价地址
    comments_count = scrapy.Field()  # 回复数
    attitudes_count = scrapy.Field() # 点赞数


class Jd2Item(scrapy.Item):
    _id = scrapy.Field()             # id
    good_id = scrapy.Field()         # 商品id
    name = scrapy.Field()            # 商品名称
    commit = scrapy.Field()          # 评价数
    price = scrapy.Field()           # 价格
    img = scrapy.Field()             # 商品图片
    detail_url = scrapy.Field()      # 详情页url
    comments = scrapy.Field()