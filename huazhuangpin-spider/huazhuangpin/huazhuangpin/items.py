# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HuazhuangpinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shop_price = scrapy.Field()
    shop_title = scrapy.Field()
    shop_category_1 = scrapy.Field()
    shop_category_2 = scrapy.Field()
    shop_brand = scrapy.Field()
    shop_fuzhi = scrapy.Field()
    shop_like = scrapy.Field()
    shop_love = scrapy.Field()
    shop_comment_amount = scrapy.Field()
    shop_comment = scrapy.Field()
