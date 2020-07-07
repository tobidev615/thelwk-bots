# -*- coding: utf-8 -*-

import scrapy
from dateutil.parser import parse


def list_controller(s):
    empty = ''
    return empty.join(s)

def vandate_controller(value):
    newer = value.split("+")[0]
    dt = parse(newer, fuzzy=True)
    return str(dt)


class VanguardUpdateSpider(scrapy.Spider):

    custom_settings = {
        'ITEM_PIPELINES': {
            'newsboy.pipelines.VangaurdNewsPipeline': 300,
        }
    }

    name = 'vanguard'
    allowed_domains = ['www.vanguardngr.com']
    start_urls = start_urls = [
        'https://www.vanguardngr.com/category/national-news/',
        'https://www.vanguardngr.com/category/sports/',
        'https://www.vanguardngr.com/category/politics/',
        ]

    def parse(self, response):
        bigbox_list=response.xpath("//main[@id='main']/article")
        page_number = response.url
        if 'www.vanguardngr.com/category/national-news/' in response.url:
            cat = 'national-news'
        elif 'www.vanguardngr.com/category/sports/' in response.url:
            cat = 'sports'
        elif 'www.vanguardngr.com/category/politics/' in response.url:
            cat = 'sports'
        else:
            cat ='unknow-category'

        for items in bigbox_list:

            headers=items.xpath(".//div[@class='rtp-post-content']/header/h2/a/text()").get()
            short_story=items.xpath(".//div[@class='rtp-post-content']/div/p/text()").get()
            news_image=items.xpath(".//div[@class='rtp-post-thumbnail']/a/img/@src").get()
            news_link=items.xpath(".//div[@class='rtp-post-content']/header/h2/a/@href").get()
            page_number=response.xpath("//span[@class='page-numbers current']/text()").get()


            yield response.follow(url=news_link, callback=self.parse_story, meta={
                'news_title': headers, 
                'brief_story': short_story, 
                'news_pic': news_image,
                'page' : page_number,
                'category': cat
                }
            )
        next_page=response.xpath("//nav[@class='rtp-pagination']/a[@class='next page-numbers']/@href").get()

        page_num = int("".join(filter(str.isdigit, next_page)))
        if page_num < 20:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_story(self, response):
        news_source = 'VANGUARD_NEWS'
        news_tag= response.meta['category']
        news_title = response.meta['news_title']
        brief  = response.meta['brief_story']
        pic_link = response.meta['news_pic']
        pager = response.meta['page']
        news_body = response.xpath("//div[@class='entry-content']/p/text()").getall()
        news_time = response.xpath("//time[@class='entry-date published']/@datetime").get()
        #news_date = response.xpath("//time[@class='entry-date published']/text()").get()
        # news_tag = response.xpath("//span[@class='rtp-meta-cat meta-tag']/a/text()").getall()
        news_link = response.url
        reaction = response.xpath("//span[@class='comment-count']/text()").get()
        try:
            page = int("".join(filter(str.isdigit, pager)))
        except:
            page = 1
        #logging.info(response.request.headers)
        yield{
            'title': news_title,
            'date' : vandate_controller(news_time),
            'pic' : pic_link,
            'brief' : brief,
            'full_story' : list_controller(news_body),
            'news_Link' : news_link,
            'tags' : news_tag,
            'source': news_source,
            'page' : page,
        }
