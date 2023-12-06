from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from database.data import BotDB
import time

url = "https://ru.skelbiu.lt/"

db = BotDB()
driver = Driver(uc=True)

while True:
    selectors = db.get_selectors()
    
    if not selectors:
        break
    
    for selector in selectors:
        for i in range(10):
            link = db.get_link(category=selector[1], under_category=selector[2], city=selector[3], page=i)
            print(link)
            time.sleep(1)
            i += 1
            try:
                driver.maximize_window()
                driver.get(link)
                time.sleep(10)
                
                agree_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
                agree_btn.click()
                time.sleep(5)
                
            except Exception as e:
                print(e)
    
    #try:
    #    driver.maximize_window()
    #    driver.get(url)
    #    time.sleep(10)

    #    agree_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    #    agree_btn.click()
    #    time.sleep(5)
    
    #except Exception as e:
    #    print(e)   
    #    
    #finally:
    #    driver.quit()
    
def update_categories():
    try:
        driver.get('https://ru.skelbiu.lt/')
        time.sleep(10)

        agree_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        agree_btn.click()
        time.sleep(5)
        
        categories = driver.find_elements(By.CSS_SELECTOR, 'a.titleHeader')
    
        for link in categories:
            href_value = link.get_attribute('href')
            print(f"Text: {link.text} Link: {href_value}")
            db.new_category(name=link.text, link=href_value)
            
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
    
def update_under_categories():
    try:
        driver.get('https://ru.skelbiu.lt/')
        time.sleep(10)
        
        agree_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        agree_btn.click()
        time.sleep(5)
        
        under_categories = driver.find_elements(By.CLASS_NAME, 'categBlock')
    
        for element in under_categories:
            category_element = element.find_element(By.CSS_SELECTOR, 'h2')
            category = category_element.text.strip()

            links = element.find_elements(By.CSS_SELECTOR, 'a')

            for link in links:
                href_value = link.get_attribute('href')
                print(f"Text_1: {link.text} Link: {href_value} Category: {category}")
                db.new_under_category(name=link.text, link=href_value, category=category)
                
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
        
def update_cities():
    try:
        driver.get(url)
        time.sleep(20)
        
        agree_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        agree_btn.click()
        time.sleep(5)

        cities_btn = driver.find_element(By.ID, 'selectboxCities')
        cities_btn.click()
        time.sleep(5)

        cities_list = driver.find_elements(By.CLASS_NAME, 'smallCity')    
        for city in cities_list:
            city_text = city.text
            try:
                city_number = city.find_element(By.CSS_SELECTOR, 'label')
            except:
                pass
            if city.text:
                city_num = city_number.get_attribute('id')
                num = city_num.replace('cityText', '')
                print(city_text, num)
                db.new_city(city=city_text, uniq_id=num)     
    except Exception as e:
        print(e)
        
    finally:
        driver.close()
        driver.quit()