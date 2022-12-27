# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

# Import Item class created for the project
from newsboy.items import NewsboyItem


# Converts date in the format of '8th August, 2021' to datetime format

def date_converter(datey):
    new = datey.split(',')
    new_date = new[1] + new[2]
    news = new_date.replace(' | ' , '')
    latest = datetime.strptime(news, " %B %d %Y %I:%M %p")
    return str(latest)

# The news body comes out as a list so this helps to change the list to string 
# Also to replace newline characters \n with <br> and \xa0 with &nbsp;

def list_controller(s):
    empty = ''
    strlist=empty.join(s)
    formattedtext1= strlist.replace('\n',' <br>')
    formattedtext2= formattedtext1.replace('\xa0',' &nbsp;')
    return formattedtext2

def int_controller(value):
    new_value = int("".join(filter(str.isdigit, value)))
    return new_value

class PmUpdateSpider(scrapy.Spider):
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'newsboy.pipelines.AllNewsPipeline': 300,
    #     }
    # }
  # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'newsboy.pipelines.PMNewsPipeline': 300,
    #     }
    # }

    name = 'pmnews'
    allowed_domains = ['pmnewsnigeria.com']
    start_urls = [ 
        'https://pmnewsnigeria.com/category/news/politics/',
        ]

    #'https://www.pmnewsnigeria.com/category/news/',
    #'https://www.pmnewsnigeria.com/category/news/metro/',
    #'https://www.pmnewsnigeria.com/category/headlines/',
    #'https://www.pmnewsnigeria.com/category/sports/',       

    def parse(self, response):
        big_box = response.xpath("//div[@class='row archive-grid']/a")

        # I had to put politics first 
        # The "In" keyword keeps seeing /news/politics as "news" instead of politics
        if 'politics' in response.url:
            cat = 'politics'
        elif 'headlines' in response.url:
            cat = 'news'
        elif 'metro' in response.url:
            cat = 'news'
        elif 'news' in response.url:
            cat = 'news'
        elif 'sports' in response.url:
            cat = 'sports'
        else:
            cat ='unknown'
        

        for items in big_box:
            page = items.xpath("//div[@class='category-pagination']//span[@class='page-numbers current']/text()").get()
            link = items.xpath("./@href").get()
            title = items.xpath(".//h3[@class='archive-grid-single-title']/text()").get()            
            #img_link = items.xpath(".//div[@class='thumbnail  election-list archive']/a/img/@src").get()

            yield response.follow(url=link, callback =self.parse_news, meta={'news_title': title, 'page': page, 'link': link, 'category':cat} )
            
        next_page=response.xpath("//a[@class='next page-numbers']/@href").get()
        
        #remove number from page link so you can know how many pages you are on and use to throtle looping.
        page_num = int("".join(filter(str.isdigit, next_page)))

        # Run every 6 hours
        if page_num < 2: 
            yield scrapy.Request(url=next_page, callback=self.parse)



    def parse_news(self, response):
        items = NewsboyItem()

        items['title'] = response.request.meta['news_title']
        items['sourcecategory'] = response.meta['category']
        pager=response.meta['page']

        try:
            page = int("".join(filter(str.isdigit, pager)))
        except:
            page = 1

        items['page'] = page
        items['link'] = response.meta['link']
        items['body']= response.xpath("//div[@class='article-content']//p/text()").getall()
        items['media']= response.xpath("//div[@class='main-article']/img/@src").get()
        items['date'] = response.xpath("//p[@class='date']/text()").get()
        items['source'] = 'PM_NEWS'
        # news_time = news_caption
        # news_body= list_controller(news_bodyraw)
        #reaction =  str(news_caption[1])

        yield items

        # yield{
        #     'title': news_head,
        #     'source-category': cat,
        #     'app-category': " ",
        #     'tags' : "",
        #     'brief': news_body[:255],
        #     'body': news_body,
        #     'media': img_link,
        #     'date': news_time,
        #     'source': source,
        #     'link': linker,
        #     'page': page,
        #     'location': "",
        #     'thelwkid': "",
        # }
        
