# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import dateparser


def list_controller(s):
    empty = ''
    re = empty.join(s)
    return re.strip()


def date_controller(value):
    # We are using this function to control dates in words and string format
    rawdate = dateparser.parse(value)
    return rawdate.strftime("%Y-%m-%d")


class ConciseUpdateSpider(scrapy.Spider):
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'newsboy.pipelines.ConciseNewsPipeline': 300,
    #     }
    # }

    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'newsboy.pipelines.AllNewsPipeline': 300,
    #     }
    # }

    name = 'conciseng'
    allowed_domains = ['concise.ng']
    start_urls = [
        'https://concise.ng/category/politics/',
        'https://www.concise.ng/category/news/'
    ]

    def parse(self, response):
        big_box = response.xpath("//*[@id='posts-container']/li")
        nextpage_link = response.xpath('//*[@id="main-content-row"]/div/div[2]/div/span[2]/a/@href').get()

        # We would derive our page number from the page link
        # current design doesn't have page number,so we would be deriving it by next page minus 1
        nextpage_number = int("".join(filter(str.isdigit, nextpage_link)))
        page_number = nextpage_number - 1

        if 'concise.ng/category/politics/' in response.url:
            cat = 'politics'
        elif 'concise.ng/category/news/' in response.url:
            cat = 'news'
        else:
            cat = 'unknown'

        for items in big_box:
            news_link = items.xpath('.//h2/a/@href').get()
            title = items.xpath(".//h2/a/text()").get()
            thumb = items.xpath(".//img/@src").get()

            yield response.follow(url=news_link, callback=self.parse_news, meta={
                'title': title,
                'link': news_link,
                'thumb': thumb,
                'page': page_number,
                'category': cat
            })
        # next_page = response.xpath("//*[@id='main-content-row']/div/div[2]/div/span[2]/a/@href").get()
        page_num = int("".join(filter(str.isdigit, nextpage_link)))

        # Run every 12 hours 
        # if page_num < 4:
        #     yield scrapy.Request(url=nextpage_link, callback=self.parse)

    def parse_news(self, response):
        title = response.meta['title']
        pager = response.meta['page']
        link = response.meta['link']
        thumb = response.meta['thumb']
        tag = response.meta['category']

        # Try was used to correct errors from the page not appearing as an integer

        media = str(response.xpath("//*[@class='featured-area-inner']//img/@src").get())
        body = list_controller(response.xpath("//div[@class='entry-content entry clearfix']//p/text()").getall())
        source = 'conciseng_news'
        date = response.xpath("//*[@id='single-post-meta']/span[2]/text()").get()

        yield {
            'title': title.strip(),
            'page': pager,
            'link': link,
            'brief': body[0:200],
            'body': body,
            'date': date_controller(date),
            'image': thumb,
            'media': media,
            'category': tag,
            'source': source
        }
