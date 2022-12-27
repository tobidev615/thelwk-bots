# -*- coding: utf-8 -*-
import scrapy
from dateutil.parser import parse

def list_controller(s):
    s.pop(0)
    empty = ''
    re = empty.join(s)
    final = re.split("Copyright PUNCH")
    return final[0].strip()
    
def vandate_controller(value):
    newer = value.split("+")[0]
    dt = parse(newer, fuzzy=True)
    return str(dt)

class PunchUpdateSpider(scrapy.Spider):
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'newsboy.pipelines.PunchNewsPipeline': 300,
    #     }
    # }

    custom_settings = {
        'ITEM_PIPELINES': {
            'newsboy.pipelines.AllNewsPipeline': 300,
        }
    }
    
    name = 'punchnews'
    allowed_domains = ['punchng.com']
    start_urls = [
        'https://punchng.com/topics/sports/',
        'https://punchng.com/all-posts/',
        'https://punchng.com/topics/top-stories/',
        'https://punchng.com/topics/latest-news/',
        'https://punchng.com/topics/metro-plus/',
        'https://punchng.com/topics/news/'
        'https://punchng.com/topics/politics/'
        ]

    def parse(self, response):
        big_box = response.xpath("//div[@class='cards no-gutter']/div")

        if 'punchng.com/topics/sports/' in response.url:
            cat = 'sports'
        elif 'punchng.com/all-posts/' in response.url:
            cat = 'news'
        elif 'punchng.com/topics/top-stories/' in response.url:
            cat = 'news'
        elif 'punchng.com/topics/latest-news/' in response.url:
            cat = 'news'
        elif 'punchng.com/topics/metro-plus/' in response.url:
            cat = 'news'
        elif 'punchng.com/topics/politics/' in response.url:
            cat = 'politics'
        elif 'punchng.com/topics/news/page/' in response.url:
            cat = 'news'
        
        else:
            cat ='unknown'

        for items in big_box:
            news_link= items.xpath("./a/@href").get()
            page = items.xpath("//div[@class='paginations']/span[@class='page-numbers current']/text()").get()
            title = items.xpath(".//h2/text()").get()
            brief = items.xpath(".//div[@class='seg-summary']/p/text()").get()

            yield response.follow(url=news_link, callback =self.parse_news, meta={'title': title, 'page': page, 'link': news_link, 'brief': brief, 'cat': cat} )

        next_page=response.xpath("//a[@class='next page-numbers']/@href").get()
        page_num = int("".join(filter(str.isdigit, next_page)))
        
        # Run every 6 hours 
        if page_num < 5: 
            yield scrapy.Request(url=next_page, callback=self.parse)
    
    def parse_news(self, response): 
        title = response.meta['title']
        pager = response.meta['page']
        link= response.meta['link']
        brief = response.meta['brief']
        tags = response.meta['cat']
        body = response.xpath("//div[@class='entry-content']//p//descendant-or-self::*/text()").getall()
        #body = response.xpath("//div[@class='entry-content']/p[@style='text-align: justify;']/descendant-or-self::*/text()").getall()
        date = response.xpath("//time/@datetime").get()
        image =response.xpath("//div[@class='row post_featured_image']//div[@class='b-lazy']/@data-src").get()
        # tag = response.xpath("normalize-space(//span[@class='post-cat-links']/a/text())").get()
        source = 'punch_news'
        try:
            page = int("".join(filter(str.isdigit, pager)))
        except:
            page = 1

        yield {
            'title': title,
            'page': page,
            'link': link,
            'brief': brief[:250],
            'body': list_controller(body),
            'date': vandate_controller(date),
            'image': image,
            'media': 'nomedia',
            'category': tags,
            'source': source
        }


