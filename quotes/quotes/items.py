# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesItem(scrapy.Item):
    quotes = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class ProductItems(scrapy.Item):
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    regular_price = scrapy.Field()
    discounted_price = scrapy.Field()
    image = scrapy.Field()
    product_available = scrapy.Field()
