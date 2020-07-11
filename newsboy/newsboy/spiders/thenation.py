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


class ThenationUpdateSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'newsboy.pipelines.TheNationNewsPipeline': 300,
        }
    }
    name = 'thenation'
    allowed_domains = ['thenationonlineng.net']
    start_urls = [
        'https://thenationonlineng.net/category/news/',
        'https://thenationonlineng.net/category/politics/',
        'https://thenationonlineng.net/category/sports2/sports-news/',
        'https://thenationonlineng.net/category/news-update/',
        'https://thenationonlineng.net/category/featured/',
        'https://thenationonlineng.net/category/city-beats/'
        ]

    def parse(self, response):
        big_box = response.xpath("//div[@class='jeg_main_content jeg_column col-sm-8']//article")
        if 'thenationonlineng.net/category/news/' in response.url:
            cat = 'news1'
        elif 'thenationonlineng.net/category/politics/' in response.url:
            cat = 'politics'
        elif 'thenationonlineng.net/category/sports2/sports-news/' in response.url:
            cat = 'sports'
        elif 'thenationonlineng.net/category/news-update/' in response.url:
            cat = 'news-update'
        elif 'thenationonlineng.net/category/featured/' in response.url:
            cat = 'featured'
        elif 'thenationonlineng.net/category/city-beats/' in response.url:
            cat = 'city-beats'
        
        else:
            cat ='unknown-category'

        for items in big_box:
            news_link= items.xpath(".//h3[@class='jeg_post_title']/a/@href").get()
            page = response.url
            title = items.xpath(".//h3[@class='jeg_post_title']/a/text()").get()
            brief = items.xpath(".//div[@class='jeg_post_excerpt']/p/text()").get()
            thumb = items.xpath(".//img/@data-src").get()
            date = items.xpath(".//div[@class='jeg_meta_date']/a/text()").get()
            reaction = items.xpath(".//div[@class='jeg_meta_comment']/descendant::*/text()").getall()

            yield response.follow(url=news_link, callback=self.parse_news, meta={
                'title': title,
                'page': page,
                'link': news_link,
                'brief': brief,
                'thumb': thumb,
                'date': date,
                'reaction': reaction,
                'category': cat
            })

        next_page = response.xpath("//a[@class='page_nav next']/@href").get()        
        page_num = int("".join(filter(str.isdigit, next_page)))
        # Run every 6 hours
        if page_num < 10: 
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_news(self, response):
        title = response.meta['title']
        pager = response.meta['page']
        link= response.meta['link']
        brief = response.meta['brief']
        thumb= response.meta['thumb']
        date = response.meta['date']
        reaction = response.meta['reaction']
        tag= response.meta['category']
        try:
            page = int("".join(filter(str.isdigit, pager)))
        except:
            page = 1

        body = response.xpath("//div[@class='content-inner ']/p/descendant-or-self::*/text()").getall()
        source='thenation_news'

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
