# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
import time
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
import datetime
from datetime import datetime
import logging
import secrets
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

key1 =range(10, 25)
key2 = range(2,8)
key3 = range(0,3)


def list_controller(stre):
    if stre == None:
        pass
    else:
        empty = ''
        str3=empty.join(stre)
        str2 = str3.replace('·', '')
        return str2

def link_controller(value):
    if value == None:
        pass
    else:
        #controls tweet with # so it doesn't affect the links
        str2= value.replace('#', '')
        return str2


class TrendsngSpider(scrapy.Spider):
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'project2sel.pipelines.localTrendPipeline': 300,
    #     }
    # }
    name = 'trendsng'
    def start_requests(self): 
        yield SeleniumRequest(
            url = 'https://mobile.twitter.com/login',
            wait_time = 3,
            callback = self.parse,
        )

    def parse(self, response):
        now=datetime.now() 
        timer=now.strftime("%Y-%m-%d")

        counter = 0
        driver = response.meta['driver']

        time.sleep(10)
        html2= driver.page_source
        logging.info(html2)
        login_box = driver.find_element_by_xpath("(//input[@name='session[username_or_email]'])[1]")
        login_box.send_keys('samonson0616')

        time.sleep(2)

        pw_box = driver.find_element_by_xpath("(//input[@name='session[password]'])[1]")
        pw_box.send_keys('Olaoluwa0615')
        time.sleep(2)

        pw_box.send_keys(Keys.ENTER)
        time.sleep(secrets.choice(key2))
        scroll = driver.find_element_by_tag_name('html')
        scroll.send_keys(Keys.END)
        time.sleep(secrets.choice(key3))
        scroll.send_keys(Keys.ARROW_DOWN)
        time.sleep(secrets.choice(key2))


        driver.get("https://mobile.twitter.com/i/trends/")
        time.sleep(secrets.choice(key1))
        time.sleep(5)
        scroll = driver.find_element_by_tag_name('html')
        scroll.send_keys(Keys.END)
        time.sleep(5)
        html=driver.page_source
        res = Selector(text=html)
        
        result_row=res.css("div.css-1dbjc4n.r-my5ep6.r-qklmqi.r-1adg3ll")
        
        for link in result_row:
            counter = counter + 1
            result = link.xpath(".//descendant::*/text()").getall()

            trend_type = link.css(".css-1dbjc4n.r-my5ep6.r-qklmqi.r-1adg3ll .css-901oao.r-1re7ezh.r-1qd0xha.r-n6v787.r-16dba41.r-1sf4r6n.r-bcqeeo.r-qvutc0 .css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0::text").extract()

            trend = link.css(".css-1dbjc4n.r-my5ep6.r-qklmqi.r-1adg3ll .css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-vw2c0b.r-ad9z0x.r-bcqeeo.r-vmopo1.r-qvutc0 .css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0::text").extract_first()
            
            tweeters = link.css(".css-1dbjc4n.r-my5ep6.r-qklmqi.r-1adg3ll  .css-901oao.r-1re7ezh.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-vmopo1.r-qvutc0     .css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0::text").extract_first()

            trend_text2 = link_controller(trend)
            trend_link =  'https://twitter.com/search?q={}'.format(trend_text2)
            yield{
                'trend': trend,
                'date': timer,
                'trend_type': list_controller(trend_type),
                'tweets': tweeters,
                'number': counter,
                'link': trend_link
            }

