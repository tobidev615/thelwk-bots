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
    custom_settings = {
        'ITEM_PIPELINES': {
            'newsboy.pipelines.PunchNewsPipeline': 300,
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
        'https://punchng.com/topics/news/page/'
        ]

    def parse(self, response):
        big_box = response.xpath("//div[@class='cards no-gutter']/div")

        for items in big_box:
            news_link= items.xpath("./a/@href").get()
            page = items.xpath("//div[@class='paginations']/span[@class='page-numbers current']/text()").get()
            title = items.xpath(".//h2/text()").get()
            brief = items.xpath(".//div[@class='seg-summary']/p/text()").get()

            yield response.follow(url=news_link, callback =self.parse_news, meta={'title': title, 'page': page, 'link': news_link, 'brief': brief} )

        next_page=response.xpath("//a[@class='next page-numbers']/@href").get()
        page_num = int("".join(filter(str.isdigit, next_page)))
        
        # Run every 6 hours 
        if page_num < 5: 
            yield scrapy.Request(url=next_page, callback=self.parse)
    
    def parse_news(self, response): 
        title = response.meta['title']
        page = response.meta['page']
        link= response.meta['link']
        brief = response.meta['brief']
        body = response.xpath("//div[@class='entry-content']//p//descendant-or-self::*/text()").getall()
        #body = response.xpath("//div[@class='entry-content']/p[@style='text-align: justify;']/descendant-or-self::*/text()").getall()
        date = response.xpath("//time/@datetime").get()
        image =response.xpath("//div[@class='row post_featured_image']//div[@class='b-lazy']/@data-src").get()
        tag = response.xpath("normalize-space(//span[@class='post-cat-links']/a/text())").get()
        source = 'punch_news'

        yield {
            'title': title,
            'page': int("".join(filter(str.isdigit, page))),
            'link': link,
            'brief': brief,
            'body': list_controller(body),
            'date': vandate_controller(date),
            'image': image,
            'tag': tag,
            'source': source
        }


