# -*- coding: utf-8 -*-
import scrapy
import logging

class AllEventsSpider(scrapy.Spider):
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'chartsng.pipelines.AppleChartPipeline': 300,
    #     }
    # }
    name = 'eventsng'
    allowed_domains = ['ogavenue.com.ng']
    start_urls = ['https://ogavenue.com.ng/']

    def parse(self, response):
        #logging.info("Started")
        #home = 'https://ogavenue.com.ng'
        all_states = response.xpath("//section[@class='states d-none d-sm-block my-5']/div[@class='row']/div/div/a[@class='blue font-s-1 font-weight-semi-bold']/@href").getall()
        for states in all_states:
            
            yield response.follow(url=states, callback = self.parse_event)

    def parse_event(self, response):
        logging.warning(response.url)
        event_row= response.xpath("//div[@class='d-flex position-relative border flex-column flex-md-row']")
        last_page = int(response.xpath("(//nav/ul/li[@class='page-item']/a)[last()]/text()").get())

        for items in event_row:
            link= items.xpath(".//div[@class='details width-md-65 p-2 d-flex flex-column justify-content-between']//h2/a/@href()").get()
            name = items.xpath(".//div[@class='details width-md-65 p-2 d-flex flex-column justify-content-between']//span[@itemprop='name']/text()").get()
            Locaton = items.xpath(".//div[@class='details width-md-65 p-2 d-flex flex-column justify-content-between']//div[@itemprop='addressLocality']/a[1]/text()").get()
            State = items.xpath(".//div[@class='details width-md-65 p-2 d-flex flex-column justify-content-between']//div[@itemprop='addressLocality']/a[2]/text()").get()
            Guests = items.xpath(".//div[@class='details width-md-65 p-2 d-flex flex-column justify-content-between']//div[@class='capacity text-md-right']/span/span[1]/text()").get()
            features = items.xpath(".//div[@class='details width-md-65 p-2 d-flex flex-column justify-content-between']//div[@class='amenities']/div/@data-content").getall()
            images = items.xpath(".//a//div[@class='image-slider position-relative']/div/div[@class='image-div']/img/@data-lazy").getall()
            logging.info(last_page)
            yield{
                'Name': name,
                'Features': features,
                'Link': link,
                'City': Locaton,
                'State': State,
                'Guests': Guests,
                'Images': images

            }
            for i in range(2, last_page):
                adder = str(i)                
                next_page = response.url + adder
                yield response.follow(url = next_page, callback = self.parse_event)
    
