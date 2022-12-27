from selenium import webdriver
import time
import logging
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument('--headless')
options.add_argument("--disable-extensions")
options.add_argument('start-maximized')
options.add_argument('--disable-gpu')
options.add_argument('--enable-automation')
options.add_argument('--disable-infobars')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--user-agent=""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36""')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path="/home/ubuntu/bots/webdrivers/chromedriver_83osx", chrome_options=options)
#driver.get("https://duckduckgo.com")
time.sleep(5)
driver.get("https://mobile.twitter.com")
#time.sleep(5)
driver.save_screenshot('new_chromeshot.png') 
html=driver.page_source
print(driver.execute_script("return navigator.userAgent"))
logging.info(html)
print(html)

driver.quit()
