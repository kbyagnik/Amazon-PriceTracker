# -*- coding: utf-8 -*-

# Scrapy settings for aragog project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'aragog'

SPIDER_MODULES = ['aragog.spiders']
NEWSPIDER_MODULE = 'aragog.spiders'
DEPTH_LIMIT = 1


ITEM_PIPELINES = ['aragog.pipelines.MongoDBPipeline', ]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "amazon"
MONGODB_COLLECTION = "products"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'aragog (+http://www.yourdomain.com)'
