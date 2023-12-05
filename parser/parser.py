from seleniumbase import Driver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

url = "https://ru.skelbiu.lt/"

driver = Driver(uc=True)

try:
    driver.maximize_window()
    driver.get(url)
    time.sleep(15)
    
    
    category_block = driver.find_element(By.ID, 'main-categories-container')
    print(category_block.text)
    links = driver.find_elements(By.CSS_SELECTOR, 'a.titleHeader')

    for link in links:
        href_value = link.get_attribute('href')
        print(f"Link: {href_value} {link.text}")
        

    under_links = driver.find_elements(By.CLASS_NAME, 'categlist')

    
    for under_link in under_links:
        value = link.get_attribute('href')
        print(f"{under_link.text} - {value} -")

except Exception as e:
    print(e)
    
finally:
    driver.quit()
