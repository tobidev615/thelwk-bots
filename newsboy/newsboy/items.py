# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsboyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    sourcecategory = scrapy.Field()
    body=scrapy.Field()
    media=scrapy.Field()
    date=scrapy.Field()
    source=scrapy.Field()
    link=scrapy.Field()
    page=scrapy.Field()
    appcategory = scrapy.Field() 
    selftags = scrapy.Field()
    brief =scrapy.Field()
    location=scrapy.Field()
    
# Defined in this page
# app category, selftags, brief,  location
