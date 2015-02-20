# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo import MongoClient

from scrapy.conf import settings

class AragogPipeline(object):
    def process_item(self, item, spider):
    	print("_______________________________________________")
        return item

products = {}

class MongoDBPipeline(object):

	def __init__(self):
		client = MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)

		db = client[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]


	def process_item(self, item, spider):
		print("hello---------======***************************")
		if item is not None:
			if item['pid'] not in products:
					products[item['pid']] = item
					currItem = self.collection.find_one({'pid':item['pid']})
					
					if currItem is None:
						self.collection.insert(dict(item))
					else:
						currTime = currItem['timestamp']
						currPrice = currItem['price']
						newTime = currTime + item['timestamp']
						newPrice = currPrice + item['price']
						self.collection.update({'pid':currItem['pid']},{'$set':{'timestamp':newTime,'price':newPrice}})
						print currItem['price']
			print(products)
		return item
