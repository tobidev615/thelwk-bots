# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.keys import Keys
import time
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


d1 = date.today()
today = d1.strftime("%Y/%m/%d")

user = "gbaderich@gmail.com"
pwd = "gr26"


class NetflixngSpider(scrapy.Spider):

    custom_settings = {
        'ITEM_PIPELINES': {
            'project2sel.pipelines.localNetflixPipeline': 300,
        }
    }

    name = 'netflixng'
    def start_requests(self):
        yield SeleniumRequest(
            url='https://netflix.com/ng/login',
            wait_time=3,
            callback = self.parse
        )

    def parse(self, response):

        driver = response.meta['driver']
        driver.implicitly_wait(10)
        time.sleep(5)
        user_input = driver.find_element_by_xpath("//input[@id='id_userLoginId']")
        pw_input = driver.find_element_by_xpath("//input[@id='id_password']")

        user_input.send_keys(user)
        pw_input.send_keys(pwd)

        time.sleep(3)

        pw_input.send_keys(Keys.ENTER)

        time.sleep(5)
        driver.maximize_window()
        driver.get('https://www.netflix.com/SwitchProfile?tkn=FV6AM3EAMZBALLFW3B4SGC7XB4')

        time.sleep(10)
        scroll = driver.find_element_by_tag_name('html')
        scroll.send_keys(Keys.END)
        time.sleep(2)
        scroll.send_keys(Keys.ARROW_DOWN)
        time.sleep(5)
        scroll.send_keys(Keys.END)
        time.sleep(2)
        scroll.send_keys(Keys.ARROW_DOWN)
        time.sleep(5)
        scroll.send_keys(Keys.END)
        time.sleep(2)
        scroll.send_keys(Keys.ARROW_DOWN)
        time.sleep(5)
        scroll.send_keys(Keys.END)
        time.sleep(2)
        scroll.send_keys(Keys.ARROW_DOWN)
        time.sleep(5)
        
        try:
            top10_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-list-context='mostWatched']//span[@role='button']")))
            top10_button.click()
            time.sleep(5)
        except: 
            pass
        try:
            top10_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-list-context='newRelease']//span[@role='button']")))
            top10_button.click()
            time.sleep(5)
        except:
            pass

        # top10_button = driver.find_element_by_xpath("//div[@data-list-context='mostWatched']//span[@role='button']")
        # time.sleep(5)
        # top10_button.click()
        # time.sleep(2)
        

       
        html = driver.page_source
        res=Selector(text=html)

        
        top10_row = res.xpath("//div[@data-list-context='mostWatched']//div[contains(@class, 'slider-item slider-item-')]")
        popular_row =res.xpath("//div[@data-list-context='popularTitles']//div[contains(@class, 'slider-item slider-item-')]")
        trending_row =res.xpath("//div[@data-list-context='trendingNow']//div[contains(@class, 'slider-item slider-item-')]")
        new_release = res.xpath("//div[@data-list-context='newRelease']//div[contains(@class, 'slider-item slider-item-')]")
        
        
        counter1 = 1
        exception = range(11,20)
        for link in top10_row:
            rank = counter1
            name = link.xpath(".//p/text()").get()
            image = link.xpath(".//img/@src").get()
            
            counter1 = counter1 + 1
            if name == None:
                continue
            elif rank in exception:
                continue
            else:
                yield{
                    'date': today,
                    'category': 'top10',
                    'rank': rank,
                    'name': name,
                    'image': image
                }                            
        
        counter2 = 1
        for link2 in popular_row:
            rank = counter2
            name = link2.xpath(".//p/text()").get()
            image = link2.xpath(".//img/@src").get()
            
            counter2 = counter2 + 1
            if name == None:
                continue
            else:
                yield{
                    'date': today,
                    'category': 'popular',
                    'rank': rank,
                    'name': name,
                    'image': image
                }
            
        
        counter3 = 1
        for link3 in trending_row:
            rank = counter3
            name = link3.xpath(".//p/text()").get()
            image = link3.xpath(".//img/@src").get()
            
            counter3 = counter3 + 1
            if name == None:
                continue
            else:
                yield{
                    'date': today,
                    'category': 'trends',
                    'rank': rank,
                    'name': name,
                    'image': image
                }

        counter4 = 1
        for link in new_release:
            rank = counter4
            name = link.xpath(".//p/text()").get()
            image = link.xpath(".//img/@src").get()
            
            counter4 = counter4 + 1
            if name == None:
                continue
            else:
                yield{
                    'date': today,
                    'category': 'new_release',
                    'rank': rank,
                    'name': name,
                    'image': image
                }                     
            