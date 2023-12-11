from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from handlers import newsletter
from database.data import BotDB
import time
import asyncio

url = "https://ru.skelbiu.lt/"

async def main():
    while True:
        try:
            db = BotDB()
            with Driver(uc=True) as driver:
                while True:
                    selectors = db.get_selectors()
                    if not selectors:
                        break
                    await process_selectors(driver, selectors, db)
        except Exception as e:
            pass
        finally:
            driver.quit()
            
async def process_selectors(driver, selectors, db):
    for selector in selectors:
        link = db.get_link(category=selector[1], under_category=selector[2], city=selector[3])
        e = await process_link(driver, link, db, selector)
        if e == 'EROR':
            print(e)
            break
        
def handle_agreement(driver):
    try:
        agree_btn = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
        if agree_btn:
            agree_btn.click()
    except Exception as e:
        pass

async def process_link(driver, link, db, selector):
    try:
        driver.maximize_window()
        driver.get(link)
        handle_agreement(driver)
        await get_ad(driver, db, selector)
    except Exception as e:
        time.sleep(2)
        print(e)
        print("Бляяяяяяяяяяяя")
        return 'EROR'
        
async def process_pagination(driver, db, selector):
    while True:
        page = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'strong.pagination_selected')))
        if int(page.text) <= 10:
            
            pagination = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.pagination_link')))
            next_button = None

            for page_link in pagination:
                if page_link.text.strip() == '»':
                    next_button = page_link
                    break

            if next_button:
                next_button.click()
                await get_ad(driver, db, selector)
            else:
                return 'break'
        else:
            return 'break'
    
async def get_ad(driver, db, selector):
    while True:
        advs = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.standard-list-item')))

        if not advs:
            break
        
        for adv in advs:
            adv_content = WebDriverWait(adv, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'content-block')))
            link = adv.get_attribute('href')
            adv_city = adv.find_element(By.CLASS_NAME, 'second-dataline').text
            adv_name = WebDriverWait(adv_content, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'title'))).text 
            adv_price_line_1 = WebDriverWait(adv_content, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'price-line')))
            adv_price_line = None
            try:
                adv_price_line = WebDriverWait(adv_price_line_1, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'price'))).text
            except Exception as e:
                pass
            selectors = db.get_kw(category=selector[1], under_category=selector[2], city=selector[3])
            keywords = [keyword[1] for keyword in selectors]
            if keywords:
                for keyword in keywords:
                    if 'мин. назад' in adv_city:    
                        if keyword.lower() in adv_name.lower():
                            for i in range(1, 20):
                                if f' {i} ' in f' {adv_city} ' or adv_city.startswith(f'{i} ') or adv_city.endswith(f' {i}'):
                                    exists = db.add_adv(name=adv_name, city=adv_city, link=link)
                                    if exists:
                                        if adv_price_line:
                                            adv_price = f'Цена: {adv_price_line}'
                                            await newsletter.handler(name=adv_name, price=adv_price, city=adv_city, link=link)
                                        else:
                                            adv_price = 'Цена: не указана'
                                            await newsletter.handler(name=adv_name, price=adv_price, city=adv_city, link=link)
                                        await asyncio.sleep(0.5)
                                i += 1
            else:
                break
        br = await process_pagination(driver, db, selector)
        if br == 'break':
            break
        
    return 'break'
        
           # print(f'{adv.text} - {link}')
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
    
#def update_categories():
#    try:
#        driver.get('https://ru.skelbiu.lt/')
#        time.sleep(10)
#
#        agree_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
#        agree_btn.click()
#        time.sleep(5)
#        
#        categories = driver.find_elements(By.CSS_SELECTOR, 'a.titleHeader')
#    
#        for link in categories:
#            href_value = link.get_attribute('href')
#            print(f"Text: {link.text} Link: {href_value}")
#            db.new_category(name=link.text, link=href_value)
#            
#    except Exception as e:
#        print(e)
#    finally:
#        driver.close()
#        driver.quit()
#    
#def update_under_categories():
#    try:
#        driver.get('https://ru.skelbiu.lt/')
#        time.sleep(10)
#        
#        agree_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
#        agree_btn.click()
#        time.sleep(5)
#        
#        under_categories = driver.find_elements(By.CLASS_NAME, 'categBlock')
#    
#        for element in under_categories:
#            category_element = element.find_element(By.CSS_SELECTOR, 'h2')
#            category = category_element.text.strip()
#
#            links = element.find_elements(By.CSS_SELECTOR, 'a')
#
#            for link in links:
#                href_value = link.get_attribute('href')
#                print(f"Text_1: {link.text} Link: {href_value} Category: {category}")
#                db.new_under_category(name=link.text, link=href_value, category=category)
#                
#    except Exception as e:
#        print(e)
#    finally:
#        driver.close()
#        driver.quit()
#        
#def update_cities():
#    try:
#        driver.get(url)
#        time.sleep(20)
#        
#        agree_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
#        agree_btn.click()
#        time.sleep(5)
#
#        cities_btn = driver.find_element(By.ID, 'selectboxCities')
#        cities_btn.click()
#        time.sleep(5)
#
#        cities_list = driver.find_elements(By.CLASS_NAME, 'smallCity')    
#        for city in cities_list:
#            city_text = city.text
#            try:
#                city_number = city.find_element(By.CSS_SELECTOR, 'label')
#            except:
#                pass
#            if city.text:
#                city_num = city_number.get_attribute('id')
#                num = city_num.replace('cityText', '')
#                print(city_text, num)
#                db.new_city(city=city_text, uniq_id=num)     
#    except Exception as e:
#        print(e)
#        
#    finally:
#        driver.close()
#        driver.quit()
        
#if __name__ == '__main__':
#    asyncio.run(main())
    