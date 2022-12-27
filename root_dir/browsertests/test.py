from selenium import webdriver
import time
import logging
from selenium.webdriver.firefox.options import Options


options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(executable_path="/home/ubuntu/bots/webdrivers/geckodriver", firefox_options=options)

driver.get("https://twitter.com/login")
time.sleep(5)
driver.save_screenshot('new_screenshot.png') 
html=driver.page_source
logging.info(html)
print(html)

driver.quit()
