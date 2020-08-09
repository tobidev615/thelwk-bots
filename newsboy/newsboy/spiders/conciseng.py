# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
from dateutil.parser import parse


def list_controller(s):
    empty = ''
    re = empty.join(s)
    return re.strip()
    
def vandate_controller(value):
    newer = value.split("+")[0]
    dt = parse(newer, fuzzy=True)
    return str(dt)

def wordate_controller(value):
    dt = parse(value, fuzzy=True)
    return str(dt)

class ConciseUpdateSpider(scrapy.Spider):
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'newsboy.pipelines.ConciseNewsPipeline': 300,
    #     }
    # }

    custom_settings = {
        'ITEM_PIPELINES': {
            'newsboy.pipelines.AllNewsPipeline': 300,
        }
    }
    name = 'conciseng'
    allowed_domains = ['www.concise.ng']
    start_urls = [
        'https://www.concise.ng/politics/',
        'https://www.concise.ng/news/'
        ]


    def parse(self, response):
        big_box = response.xpath("//section[@class='cat-page-section']/div[@class='container']/child::div/div/div[@class='post-line-wraper clearfix']")
        page = response.xpath("//span[@class='current']/text()").get()

        if 'www.concise.ng/politics/' in response.url:
            cat = 'politics'
        elif 'www.concise.ng/news/' in response.url:
            cat = 'news'
        else:
            cat ='unknown'

        for items in big_box:
            news_link= items.xpath(".//h3/a/@href").get()
            title = items.xpath(".//h3/a/text()").get()
            thumb = items.xpath(".//div[@class='flex-col post-image']//img/@data-src").get()

            yield response.follow(url=news_link, callback=self.parse_news, meta={
                'title': title,
                'page': page,
                'link': news_link,
                'thumb': thumb,
                'category': cat
            })
        next_page=response.xpath("//a[@class='nextpostslink']/@href").get()
        page_num = int("".join(filter(str.isdigit, next_page)))

        # Run every 12 hours 
        if page_num < 4: 
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_news(self, response):
        title = response.meta['title']
        pager = response.meta['page']
        link= response.meta['link']
        thumb= response.meta['thumb']
        tag= response.meta['category']
        try:
            page = int("".join(filter(str.isdigit, pager)))
        except:
            page = 1
        media = str(response.xpath("//section[@class='cat-page-section']//div[@class='flex-col single-post-content']/div[@class='clearfix'][1]//img/@data-src").getall())
        body = list_controller(response.xpath("//section[@class='cat-page-section']//div[@class='flex-col single-post-content']/div[@class='clearfix'][1]/p/descendant-or-self::*/text()").getall())
        source='conciseng_news'
        date = response.xpath("//section[@class='cat-page-section']//div[@class='post-meta']/text()[2]").get()

        yield {
            'title': title.strip(),
            'page': page,
            'link': link,
            'brief': body[0:200],
            'body': body,
            'date': wordate_controller(date),
            'image': thumb,
            'media': media,
            'category': tag,
            'source': source
        }
