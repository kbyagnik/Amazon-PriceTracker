import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from aragog.items import AragogItem
import datetime
from pymongo import MongoClient
from scrapy.conf import settings
from scrapy.http.request import Request

class AmazonUpdateSpider(CrawlSpider):
	name = 'aragogUpdate'
	allowed_domains = ['amazon.in']	
	start_urls = [ ]
	# rules = (
	# 	Rule(LxmlLinkExtractor(allow=(r'\/([A-Z])([A-Z0-9]{9})'),deny=(r'product\-reviews',r'offer\-listing')),callback='parse_item'),
	# 	)
		
	def __init__(self):
		client = MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)

		db = client[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def start_requests(self):
		urls = self.collection.find({},{"url":1,"_id":0})
		for url in urls:
			yield Request(url["url"], self.parse)

	def parse(self,response):
		item = AragogItem()
		try:
			item['name'] = response.xpath('//*[@id="productTitle"]/text()').extract()[0].encode('ascii','ignore')
			item['reviews'] = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract()[0].encode('ascii','ignore')
			item['url'] = response.url
			item['rating'] = response.xpath('//*[@id="avgRating"]/span/text()').extract()[0].encode('ascii','ignore').replace('\n',' ').strip()
			item['pid'] = response.url.split('/ref=')[0].split('/')[-1].encode('ascii','ignore')
			item['price'] = [response.xpath('//*[@id="price"]/table//span[starts-with(@id,"priceblock")]//text()').extract()[1].encode('ascii','ignore').strip()]
			item['desc'] = [desc.encode('ascii','ignore') for desc in response.xpath('//*[@id="feature-bullets"]/ul/li/span/text()').extract() ]
			item['timestamp'] = [str(datetime.datetime.now())]
			print(item)
		except:
			print('Not a product!')
			item = None
		yield item

	def dummy(self,response):
		print(str(response.url))