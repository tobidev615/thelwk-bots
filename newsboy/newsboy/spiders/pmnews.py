# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

def date_converter(datey):
    new = datey.split(',')
    new_date = new[1] + new[2]
    news = new_date.replace(' | ' , '')
    latest = datetime.strptime(news, " %B %d %Y %I:%M %p")
    return str(latest)

def list_controller(s):
    empty = ''
    return empty.join(s)

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
    allowed_domains = ['www.pmnewsnigeria.com']
    start_urls = [ 
        'https://pmnewsnigeria.com/category/news',
        'https://www.pmnewsnigeria.com/category/headlines/',
        'https://www.pmnewsnigeria.com/category/metro/',
        'https://www.pmnewsnigeria.com/category/politics/',
        'https://www.pmnewsnigeria.com/category/sports/'
        ]


    def parse(self, response):
        big_box = response.xpath("//div[@class='col-md-8']/div")

        if 'pmnewsnigeria.com/category/news' in response.url:
            cat = 'news'
        elif 'pmnewsnigeria.com/category/headlines/' in response.url:
            cat = 'news'
        elif 'pmnewsnigeria.com/category/metro/' in response.url:
            cat = 'news'
        elif 'pmnewsnigeria.com/category/politics/' in response.url:
            cat = 'politics'
        elif 'pmnewsnigeria.com/category/sports/' in response.url:
            cat = 'sports'
        else:
            cat ='unknown'


        for items in big_box:
            page = items.xpath("//span[@class='page-numbers current']/text()").get()
            link = items.xpath(".//div[@class='thumbnail  election-list archive']/a/@href").get()
            title = items.xpath(".//div[@class='thumbnail  election-list archive']/a/div/h4/text()").get()            
            img_link = items.xpath(".//div[@class='thumbnail  election-list archive']/a/img/@src").get()

            yield response.follow(url=link, callback =self.parse_news, meta={'news_title': title, 'img_thumb': img_link, 'page': page, 'link': link, 'category':cat} )
            
        next_page=response.xpath("//a[@class='next page-numbers']/@href").get()
        page_num = int("".join(filter(str.isdigit, next_page)))
        # Run every 6 hours
        if page_num < 5: 
            yield scrapy.Request(url=next_page, callback=self.parse)



    def parse_news(self, response):
        
        news_head = response.request.meta['news_title']
        img_thum = response.request.meta['img_thumb']
        pager = response.meta['page']
        linker = response.meta['link']
        cat = response.meta['category']
        news_body= response.xpath("//div[@class='col-md-5 post-content']/p/text()").getall()
        img_link= response.xpath("//div[@class='wp-caption alignnone']/img/@src").get()
        news_caption = response.xpath("//div[@class='col-md-12 post']/p/text()").getall()
        # tags = response.xpath("//div[@class='col-md-12 post']/p/a/text()").get()
        source = 'PM_NEWS'
        news_time = news_caption[0]
        reaction =  str(news_caption[1])
        try:
            page = int("".join(filter(str.isdigit, pager)))
        except:
            page = 1

        yield{
            'title': news_head,
            'date': date_converter(news_time),
            'brief': list_controller(news_body)[:250],
            'media': img_link,
            'image': img_thum,
            'body': list_controller(news_body),
            'link': linker,
            'category': cat,
            'source': source,
            'page': page,
            'reaction' : int_controller(reaction)
        }
        
