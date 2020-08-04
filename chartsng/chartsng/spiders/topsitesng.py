# -*- coding: utf-8 -*-
import scrapy
from datetime import date


class TopsitesngSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'chartsng.pipelines.topsitesngPipeline': 300,
        }
    }
    name = 'topsitesng'
    allowed_domains = ['alexa.com']
    start_urls = ['https://www.alexa.com/topsites/countries/NG']

    def parse(self, response):
        today = date.today()
        dater = today.strftime("%Y-%m-%d")

        bigbox = response.xpath("//div[@class='listings table']/div[@class='tr site-listing']")

        for rows in bigbox:
            rank = rows.xpath("./div[@class='td']/text()").get()
            sitename = rows.xpath("./div[@class='td DescriptionCell']/p/a/text()").get()
            others=rows.xpath("./div[@class='td right']/p/text()").getall()
            dailytime= others[0]
            pageviews= others[1]
            searchtraffic= others[2]
            siteslink= others[3]

            yield{
                'date': dater,
                'rank': rank,
                'website': 'www.' + sitename.lower(),
                'timeonsite': dailytime,
                'pageviews': pageviews,
                'searchtraffic': searchtraffic,
                'siteslink': siteslink
            }

            

            