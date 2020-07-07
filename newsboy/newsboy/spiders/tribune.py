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


class TribuneUpdateSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'newsboy.pipelines.TribuneNewsPipeline': 300,
        }
    }
    name = 'tribune'
    allowed_domains = ['tribuneonlineng.com']
    start_urls = [
        'https://tribuneonlineng.com/category/latest-news/',
        ]

    def parse(self, response):
        big_box = response.xpath("//div[@class='listing listing-blog listing-blog-1 clearfix  columns-1']/article")

        for items in big_box:
            news_link= items.xpath(".//h2[@class='title']/a/@href").get()
            page = response.url
            title = items.xpath(".//h2[@class='title']/a/text()").get()
            brief = items.xpath(".//div[@class='post-summary']/text()").get()
            thumb = items.xpath(".//div[@class='featured clearfix']/a/@data-src").get()
            date = items.xpath(".//div[@class='post-meta']/span[@class='time']/time/@datetime").get()

            yield response.follow(url=news_link, callback=self.parse_news, meta={
                'title': title,
                'page': page,
                'link': news_link,
                'brief': brief,
                'thumb': thumb,
                'date': date
            })

        next_page=response.xpath("//div[@class='older']/a/@href").get()
        page_num = int("".join(filter(str.isdigit, next_page)))

        if page_num < 50: 
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_news(self, response):
        title = response.meta['title']
        pager = response.meta['page']
        link= response.meta['link']
        brief = response.meta['brief']
        thumb= response.meta['thumb']
        date = response.meta['date']
        try:
            page = int("".join(filter(str.isdigit, pager)))
        except:
            page = 1

        body = response.xpath("//div[@class='single-container']/article/div[@class='entry-content clearfix single-post-content']/child::*[not(.//a)]/text()").getall()
        tag = response.xpath("//div[@class='term-badges ']/descendant::*/text()").get()
        source='tribune_news'

        yield {
            'title': title.strip(),
            'page': page,
            'link': link,
            'brief': brief.strip(),
            'body': list_controller(body),
            'date': vandate_controller(date),
            'image': thumb,
            'tag': tag,
            'source': source
        }