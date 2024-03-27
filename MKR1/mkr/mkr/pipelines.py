# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
import re

class MkrPipeline:
    def process_item(self, item, spider):
        return item

class PricePipeline:
    def process_item(self, item, spider):
        if 'price' in item:
            item['price'] = self.clean_price(item['price'])
        return item

    def clean_price(self, price_str):
        cleaned_price = price_str.strip()
        cleaned_price = cleaned_price.replace("\xa0", "")
        return cleaned_price


    
class NamePipeline:
    def process_item(self, item, spider):
        if 'name' in item:
            item['name'] = self.clean_name(item['name'])
        return item

    def clean_name(self, name):
        cleaned_name = name.strip()
        cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
        return cleaned_name