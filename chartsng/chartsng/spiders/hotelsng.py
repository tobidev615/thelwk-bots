# -*- coding: utf-8 -*-
import scrapy
import logging

class AllHotelsSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'chartsng.pipelines.HotelsNGPipeline': 300,
        }
    }
    name = 'hotelsng'
    allowed_domains = ['hotels.ng']
    start_urls = ['http://hotels.ng/']

    def parse(self, response):
        all_states = response.xpath("//div[@class='states-grid']/div/a/@href").getall()
        for item in all_states:
            yield response.follow(url=item, callback = self.parse_hotel)

    def parse_hotel(self, response):
        big_list = response.xpath("//div[@id='topPicks']/div[@class='listing-hotels']/div[@class='row']")
        next_page = response.xpath("//ul[@class='pagination']/li/a[@aria-label='Next Page']/@href").get()
        for hotels in big_list:
            name = hotels.xpath(".//div[@class='col-xs-12 col-sm-8 row listing-hotels-details-box']/div[@class='col-xs-8 listing-hotels-details ']/div[@class='listing-hotels-details-property']/a/h2/text()").get()
            hotel_link = hotels.xpath(".//div/div/div[@class='listing-hotels-slider  ']/div/a/@href").get()
            hotel_images = hotels.xpath(".//div/div/div[@class='listing-hotels-slider  ']/div/meta/@content").getall()
            city = hotels.xpath(".//div[@class='col-xs-12 col-sm-8 row listing-hotels-details-box']/div[@class='col-xs-8 listing-hotels-details ']/p[@itemprop='address']/span/a[1]/text()").get()
            state = hotels.xpath(".//div[@class='col-xs-12 col-sm-8 row listing-hotels-details-box']/div[@class='col-xs-8 listing-hotels-details ']/p[@itemprop='address']/span/a[2]/text()").get()
            address = hotels.xpath(".//div[@class='col-xs-12 col-sm-8 row listing-hotels-details-box']/div[@class='col-xs-8 listing-hotels-details ']/p[@itemprop='address']/text()").get()
            rating = hotels.xpath(".//div[@class='col-xs-12 col-sm-8 row listing-hotels-details-box']/div[@class='col-xs-4 listing-hotels-prices ']/div[@class='listing-hotels-rating-box']/p/span/text()").get()
            features = hotels.xpath(".//div[@class='col-xs-12 col-sm-8 row listing-hotels-details-box']/div[@class='col-xs-8 listing-hotels-details ']/div[@class='listing-hotels-facilities hidden-xs']/div/p/text()").getall()
            new_price = hotels.xpath(".//div[@class='col-xs-12 col-sm-8 row listing-hotels-details-box']/div[@class='col-xs-4 listing-hotels-prices ']/p[@class='listing-hotels-prices-discount']/text()").get()
            old_price = hotels.xpath(".//div[@class='col-xs-12 col-sm-8 row listing-hotels-details-box']/div[@class='col-xs-4 listing-hotels-prices ']/p[@class='listing-hotels-prices-real']/text()").get()
            
            yield{
                'Name': name,
                'Link': hotel_link,
                'Images': hotel_images,
                'City': city,
                'State': state,
                'Address': address,
                'Rate': rating,
                'Features': features,
                'New_Price': new_price,
                'Old_Price': old_price

            }
            if next_page:
                yield scrapy.Request(url=next_page, callback = self.parse_hotel)
