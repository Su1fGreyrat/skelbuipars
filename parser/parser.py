from seleniumbase import Driver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from database.data import BotDB
import time

url = "https://ru.skelbiu.lt/"

db = BotDB()
driver = Driver(uc=True)

try:
    driver.maximize_window()
    driver.get(url)
    time.sleep(15)
    
    links = driver.find_elements(By.CSS_SELECTOR, 'a.titleHeader')

    for link in links:
        href_value = link.get_attribute('href')
        print(f"Text: {link.text} Link: {href_value}")
        db.new_category(name=link.text, link=href_value)
        
except Exception as e:
    print(e)
    
finally:
    driver.quit()
