# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from dateutil.parser import parse as paars
from selenium.webdriver.common.keys import Keys
import time
import logging
import secrets

key1 =range(10, 25)
key2 = range(2,8)
key3 = range(0,3)


def hat_controller(stre):
    empty = ''
    str3=empty.join(stre)
    str2 = str3.replace('@', ' @')
    return str2

def list_controller(stre):
    empty = ''
    str3=empty.join(stre)
    str2 = str3.replace('\n', '')
    return str2

def date_corrector(value):
    new = value.split(".")
    date = paars(new[0],fuzzy=True)
    return str(date)


class TrendsngSpider(scrapy.Spider):
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'project2sel.pipelines.localTrendPipeline': 300,
    #     }
    # }
    name = 'tweetfeeder'
    
    def start_requests(self):
       
        yield SeleniumRequest(
                    url='https://mobile.twitter.com/login',
                    wait_time=15,
                    callback=self.parse
                )

    def parse(self, response):

        accounts = [
            'https://mobile.twitter.com/BashirAhmaad',
            'https://mobile.twitter.com/GarShehu',
            'https://mobile.twitter.com/fkeyamo',
            'https://mobile.twitter.com/bukolasaraki',
            'https://mobile.twitter.com/obyezeks',
            'https://mobile.twitter.com/NGRPresident',
            'https://mobile.twitter.com/HQNigerianArmy',
            'https://mobile.twitter.com/cenbank',
            'https://mobile.twitter.com/nassnigeria',
            'https://mobile.twitter.com/MBuhari',
            'https://mobile.twitter.com/atiku',
            'https://mobile.twitter.com/GovAyoFayose',
            'https://mobile.twitter.com/GEJonathan',
            'https://mobile.twitter.com/aishambuhari',
            'https://mobile.twitter.com/toluogunlesi',
            'https://mobile.twitter.com/OgbeniDipo',
            'https://mobile.twitter.com/NCDCgov',
            'https://mobile.twitter.com/LSMOH',
            'https://mobile.twitter.com/WHONigeria',
            'https://mobile.twitter.com/Fmohnigeria',
            'https://mobile.twitter.com/akandeoj',
            'https://mobile.twitter.com/elrufai',
            'https://mobile.twitter.com/abikedabiri',
            'https://mobile.twitter.com/kfayemi',
            'https://mobile.twitter.com/MrAbuSidiq',
            'https://mobile.twitter.com/raufaregbesola',
            'https://mobile.twitter.com/femigbaja',
            'https://mobile.twitter.com/abati1990',
            'https://mobile.twitter.com/jidesanwoolu',
            'https://mobile.twitter.com/officialEFCC',
            'https://mobile.twitter.com/NigeriaGov',
            'https://mobile.twitter.com/ekitistategov',
            'https://mobile.twitter.com/oyostategovt',
            'https://mobile.twitter.com/DMONigeria',
            'https://mobile.twitter.com/SenBalaMohammed',
            'https://mobile.twitter.com/followlasg',
            'https://mobile.twitter.com/YeleSowore',
            'https://mobile.twitter.com/SaharaReporters'
            'https://mobile.twitter.com/ogundamisi'
        ]
        
        # accounts = [
        #     'https://mobile.twitter.com/YeleSowore'
        # ]
        
        driver=response.meta['driver']
        try:
            login_box = driver.find_element_by_xpath("(//input[@name='session[username_or_email]'])[1]")
            login_box.send_keys('naijainfo3')

            time.sleep(2)

            pw_box = driver.find_element_by_xpath("(//input[@name='session[password]'])[1]")
            pw_box.send_keys('Olaoluwa123')

            time.sleep(2)

            pw_box.send_keys(Keys.ENTER)
            time.sleep(5)
        except:
            pass

        for items in accounts:
            time.sleep(secrets.choice(key3))
            driver.get(items)
            time.sleep(secrets.choice(key1))
            try:
                scroll = driver.find_element_by_tag_name('html')
                scroll.send_keys(Keys.END)
                time.sleep(secrets.choice(key2))
                scroll.send_keys(Keys.ARROW_DOWN)
                time.sleep(secrets.choice(key3))
                scroll.send_keys(Keys.END)
                time.sleep(secrets.choice(key2))
                scroll.send_keys(Keys.ARROW_DOWN)
                time.sleep(secrets.choice(key3))
                scroll.send_keys(Keys.END)
                time.sleep(secrets.choice(key1))
            except: 
                continue

            
            html= driver.page_source
            # logging.info(html)
            new_response = Selector(text=html)
            counter = 0
            result_row = new_response.xpath("//article[@class='css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-o7ynqc r-6416eg']")
            time.sleep(secrets.choice(key1))
            for link in result_row:
                counter = counter + 1
                try:
                    tweet_type = link.xpath(".//div[@class='css-1dbjc4n r-1habvwh r-1iusvr4 r-16y2uox']/descendant-or-self::*/text()").getall()

                    tweet_handler = link.xpath(".//div[@class='css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs r-1ny4l3l']/descendant::*/text()").getall()

                    # tweet_body = link.xpath(".//div[@class='css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0']/descendant::*/text()").getall()
                    tweet_body = link.xpath(".//div[@class='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0']/descendant::*/text()").getall()
                    timeer = link.xpath(".//div[@class='css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2']/a/time/@datetime").get()
                    tweet_link = link.xpath(".//div[@class='css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2']/a/@href").get()
                    f_link = 'https://mobile.twitter.com'+tweet_link
                    
                    tweet_media = link.xpath(".//div[@class='css-1dbjc4n r-1udh08x']")
                    tweet_vid = tweet_media.xpath(".//video/@src").getall()
                    tweet_img = tweet_media.xpath(".//img/@src").getall()
                    # tweet_type2 = list_controller(tweet_type)
                    

                    yield{
                        'number': counter,
                        'post': list_controller(tweet_body),
                        'type': str(tweet_type),
                        'poster': hat_controller(tweet_handler),
                        'videos' : str(tweet_vid),
                        'images': str(tweet_img),
                        'time': date_corrector(timeer),
                        'link': f_link,
                    }
                except :
                    continue


