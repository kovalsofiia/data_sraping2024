# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MkrItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    
class ShopItem(scrapy.Item):
    item_name =scrapy.Field()
    shop_name = scrapy.Field()
    shop_price = scrapy.Field()
    shop_url = scrapy.Field()