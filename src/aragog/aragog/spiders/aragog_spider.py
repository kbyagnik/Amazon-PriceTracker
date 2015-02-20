import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from aragog.items import AragogItem
import datetime
from scrapy.conf import settings

class AmazonSpider(CrawlSpider):
	name = 'aragog'
	allowed_domains = ['amazon.in']
	rules = (Rule(LxmlLinkExtractor(allow=(r'\/([A-Z])([A-Z0-9]{9})'),deny=(r'product\-reviews',r'offer\-listing',r'ebook')),callback='parse_item'),Rule(LxmlLinkExtractor(allow=(''))),)

	def __init__(self, start_url='http://www.amazon.in/Laptops/b/ref=nav_shopall_computers_laptop?ie=UTF8&node=1375424031',*args, **kwargs):
		super(AmazonSpider, self).__init__(*args, **kwargs)
		self.start_urls = [start_url]
	
		
	def parse_item(self,response):
		# print(str(response.url))
		item = AragogItem()
		try:
			item['name'] = response.xpath('//*[@id="productTitle"]/text()').extract()[0].encode('ascii','ignore')
			item['reviews'] = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract()[0].encode('ascii','ignore')
			item['url'] = response.url
			# print(response.xpath('//*[@id="avgRating"]/span/text()').extract())
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