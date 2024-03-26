# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import re
from lab2.items import StaffItem
import pymongo
class CleanNamePipeline:
    def process_item(self, item, spider):
        if isinstance(item, StaffItem):
            item['name'] = self.clean_name(item['name'])

        return item

    def clean_name(self, name):
        # Remove unwanted prefix using regular expressions
        cleaned_name = re.sub(r'^Завідувач кафедри:\s*', '', name)
        return cleaned_name.strip()


class MongoDBPipeline_staff:
    def open_spider(self, spider):
        # Connect to MongoDB
        self.client = pymongo.MongoClient('mongodb+srv://kovalsofiia:root@nodejs4sem.qm53cjv.mongodb.net/scraping?retryWrites=true&w=majority')
        self.db = self.client['scraping']  # Replace 'your_database' with your database name
        self.collection = self.db['scraping']  # Replace 'your_collection' with your collection name

    def close_spider(self, spider):
        # Close the MongoDB connection
        self.client.close()

    def process_item(self, item, spider):
        # Check if the item already exists in the collection
        if self.is_duplicate(item):
            # Update the existing record if needed
            self.update_item(item)
        else:
            # Insert the item into the collection
            self.insert_item(item)
        return item

    def is_duplicate(self, item):
        # Check if the item already exists in the collection based on some criteria
        query = {
            'name': item['name'],
            'department': item['department'],
            'institute': item['institute']
        }
        return self.collection.find_one(query) is not None

    def update_item(self, item):
        # Update the existing record in the collection
        query = {
            'name': item['name'],
            'department': item['department'],
            'institute': item['institute']
        }
        update_query = {
            '$set': {  # Use $set to update specific fields
            }
        }
        self.collection.update_one(query, update_query)

    def insert_item(self, item):
        # Insert the item into the collection
        self.collection.insert_one(dict(item))


class MongoDBPipeline_institute:
    def open_spider(self, spider):
        # Connect to MongoDB
        self.client = pymongo.MongoClient('mongodb+srv://kovalsofiia:root@nodejs4sem.qm53cjv.mongodb.net/scraping?retryWrites=true&w=majority')
        self.db = self.client['scraping']  # Replace 'your_database' with your database name
        self.collection = self.db['institutes']  # Replace 'your_collection' with your collection name

    def close_spider(self, spider):
        # Close the MongoDB connection
        self.client.close()

    def process_item(self, item, spider):
        # Check if the item already exists in the collection
        if self.is_duplicate(item):
            # Update the existing record if needed
            self.update_item(item)
        else:
            # Insert the item into the collection
            self.insert_item(item)
        return item

    def is_duplicate(self, item):
        # Check if the item already exists in the collection based on some criteria
        query = {
            'name': item['name'],
            'url': item['url'],
            'image_urls': item['image_urls']
        }
        return self.collection.find_one(query) is not None

    def update_item(self, item):
        # Update the existing record in the collection
        query = {
            'name': item['name'],
            'url': item['url'],
            'image_urls': item['image_urls']
        }
        update_query = {
            '$set': {  # Use $set to update specific fields
            }
        }
        self.collection.update_one(query, update_query)

    def insert_item(self, item):
        # Insert the item into the collection
        self.collection.insert_one(dict(item))
        
             
class MongoDBPipeline_department:
    def open_spider(self, spider):
        # Connect to MongoDB
        self.client = pymongo.MongoClient('mongodb+srv://kovalsofiia:root@nodejs4sem.qm53cjv.mongodb.net/scraping?retryWrites=true&w=majority')
        self.db = self.client['scraping']  # Replace 'your_database' with your database name
        self.collection = self.db['departments']  # Replace 'your_collection' with your collection name

    def close_spider(self, spider):
        # Close the MongoDB connection
        self.client.close()

    def process_item(self, item, spider):
        # Check if the item already exists in the collection
        if self.is_duplicate(item):
            # Update the existing record if needed
            self.update_item(item)
        else:
            # Insert the item into the collection
            self.insert_item(item)
        return item

    def is_duplicate(self, item):
        # Check if the item already exists in the collection based on some criteria
        query = {
            'name': item['name'],
            'url': item['url'],
            'institute': item['institute']
        }
        return self.collection.find_one(query) is not None

    def update_item(self, item):
        # Update the existing record in the collection
        query = {
            'name': item['name'],
            'url': item['url'],
            'institute': item['institute']
        }
        update_query = {
            '$set': {  # Use $set to update specific fields
            }
        }
        self.collection.update_one(query, update_query)

    def insert_item(self, item):
        # Insert the item into the collection
        self.collection.insert_one(dict(item))