AMAZON PRICE TRACKER
====================

### By Gaurav Mittal, Rahul Mittal and Kaushal Yagnik  

#### CSL707 ASSIGNMENT-3

PROBLEM DESCRIPTION
-------------------

To build an application which automate the tracking of prices of all products which are sold on a particular e-stores allowing users to analyze the trend in the prices and make some profitable decisions based on them.


APPLICATION SUMMARY
-------------------

The application is essentially a crawler which on providing a start URL and a particular depth traverses the website (Amazon.in) searching for products and scraping their corresponding webpages for the following details:

* Product Name and Description
* Product’s unique URL
* Product’s Price
* Rating
* Number of Reviews

After collecting the necessary details, they are dumped into a database collection to be used later for observing price trends through graphs and performing specific web scraping based on URLs collected.

Finally, the client interface provides the user to analyze the price trends by specifying the product URL of the product and obtain a graph of the prices recorded over the various times the webpage is crawled by the application.

SYSTEM REQUIREMENTS
-------------------

1. Python 2.7
2. Scrapy Framework (sudo pip install scrapy)
3. MongoDB
4. pyMongo (sudo pip install pymongo)
5. PHP
6. MongoDB PHP Driver (http://php.net/manual/en/mongo.installation.php)

CONTENTS
--------

1. src folder
	i. aragog - Contains crawler to scrape/parse and collect data
	ii. web - Contains files related to the client side interface

2. README - Document explaining the system requirements and how to run the application.

3. Design Document - Document explaining the design of the solution.

4. dbDump - File containing the dump of the database.


HOW TO RUN
----------

1. First of all, make sure all the requirement are met by installing all the required softwares along with their dependencies.

2. To run the crawler to crawl the entire website starting from a particular URL and upto a particular depth, go inside the src/aragog directory and run the following command:  
```$ scrapy crawl aragog -s DEPTH_LIMIT=<depth> -a start_url='<start-url'> -o <json-dump file> -t json```  
for eg.  
```$ scrapy crawl aragog -s DEPTH_LIMIT=2 -a start_url='http://www.amazon.in/gp/site-directory/ref=nav_sad' -o amazon.json -t json```  
(all -s , -a , -o and -t are option, -o and -t are for dumping json, -s to specify setting like here specifying depth of crawling and -a to specify argument like here specifying starting url for crawling)

3. If the database already contains URLs, you can run the crawler aragogUpdate to scrape specific webpages related to the URLs in the database and add new prices with timestamps of the products. For that go inside src/aragog directory and run the following:  
```$ scrapy crawl aragogUpdate```

4. Place the web folder inside localhost to host the web interface.

5. Go to the localhost from the browser to start using the web interface.

6. There you can provide the URL of a product from the website and on submitting the form obtain the graph showing the prices of the product at various points in time.


APPLICATION DESIGN
------------------

The entire application can be divided into three key components:

**1. Crawling the website and parsing the necessary details**

**2. Dumping the acquired details into the database**

**3. Using the details to plot graphs for analyzing price trends of the products**

###CRAWLING THE WEBSITE AND PARSING THE DATA

The crux of the application lies in being able to traverse through the target e-commerce website as far as possible, extracting links and visiting then and finally, obtain the relevant data by characterising the desired webpages and segments of the webpages following by parsing them suitably.

In order to accomplish this task of crawling the website and parsing/scraping for the necessary data, Scrapy is used.

**“Scrapy is an open source and collaborative python based framework for extracting the data you need from websites in a fast, simple and yet extensible way”** - <http://scrapy.org>

![Scrapy-Workflow](http://asheesh.org/pub/scrapy-talk/_images/scrapy-diagram-1.png)
Photo Source: <http://asheesh.org/pub/scrapy-talk/_images/scrapy-diagram-1.png>

The above image explains the working of Scrapy which is essentially how the application goes about crawling the website and parse for relevant data:

* Scrapy allows building custom webcrawlers and spiders which crawl the website starting from a particular starting URL and upto a particular depth, all of which can be very easily specified and customized.

* It also allows to specify certains rules based on which the crawler will decide whether the particular webpage needs to be parsed, whether it need to halt there or simple continue crawling further deep.

* Next, in case the particular web page needs to be parsed, certain parts of it are specified in terms of there xpath.

* Finally all the data that is needed is encapsulated in a set of objects serving as a representation for this data both in the form it is collected and the way it is further processed in the various pipelines.

* In this particular application, two spiders are created by the name of aragog_spider and update_spider:
    * **aragog_spider**: This spider is responsible for a complete crawling of the website starting from the set of start_urls it is provided with.
    * **update_spider**: This spider is responsible to crawl and parse on specific URLs present in the database with the aim to update the pricing of the products for trend analyzing.

* The item representing the data collected from the website is AragogItem containing details like the product ID, name, decription, price and other things.







