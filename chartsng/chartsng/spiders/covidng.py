# -*- coding: utf-8 -*-
import scrapy
import time
from datetime import date

class CovidngSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'chartsng.pipelines.CovidChartPipeline': 300,
        }
    }
    name = 'covidng'
    allowed_domains = ['covid19.ncdc.gov.ng']
    start_urls = ['https://covid19.ncdc.gov.ng/']

    def parse(self, response):
        today = date.today()
        dater = today.strftime("%Y-%m-%d")

        time.sleep(15)

        databox = response.xpath("//table[@id='custom1']/tbody/tr")

        day = dater
        
        total_test = response.xpath("normalize-space((//div[@class='page-header']//h2[@class='text-right text-white']/span/text())[1])").get()

        for rows in databox:
            
            state = rows.xpath("normalize-space(.//td[1]/text())").get()
            total_cases = rows.xpath("normalize-space(.//td[2]/text())").get()
            active_cases = rows.xpath("normalize-space(.//td[3]/text())").get()
            discharged = rows.xpath("normalize-space(.//td[4]/text())").get()
            death = rows.xpath("normalize-space(.//td[5]/text())").get()
            
            yield{
                    
                    'date' : str(day),
                    'samples_tested': total_test,
                    'state': state,
                    'total': total_cases,
                    'active': active_cases,
                    'discharged' : discharged,
                    'death': death
                
            }


            
            