# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.item import Item, Field


class AragogItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = Field()
    name = Field()
    url = Field()
    price = Field()
    timestamp = Field()
    desc = Field()
    rating = Field()
    reviews = Field()
    
