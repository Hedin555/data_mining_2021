from pprint import pprint
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['mvideo']
new_data = db.new_data

chrome_options = Options()
chrome_options.add_argument('start-maximized')
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

new_goods = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/ancestor::div[contains(@class, 'facelift')]")
actions = ActionChains(driver)
actions.move_to_element(new_goods)
actions.perform()

for i in range(5):
    button = new_goods.find_element_by_xpath(".//a[contains(@class, 'next-btn')]")
    time.sleep(5)
    button.click()

goods_data = []
goods = new_goods.find_elements_by_xpath(".//li/descendant::a")
for good in goods:
    goods_data.append(good.get_attribute('data-product-info'))
pprint(goods_data)

# не стал добавлять в базу