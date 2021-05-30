from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['mail']
mail_data = db.mail_data

chrome_options = Options()
chrome_options.add_argument('start-maximized')
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://light.mail.ru/') #подглядел про мобильную версию :)

elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "username")))
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)

elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "password")))
elem.send_keys('NextPassword172!')
elem.send_keys(Keys.ENTER)

all_links = []
while True:
    links = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//tr[contains(@class,'messageline')]")))
    links = driver.find_elements_by_xpath(".//tr[contains(@class,'messageline')]")
    for link in links:
        mail_link = link.find_element_by_xpath(".//td[@class='messageline__from messageline__item']/a[@class='messageline__link']").get_attribute('href')
        all_links.append(mail_link)
    try:
        button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Далее']")))
        button.click()
    except:
        break

#print(len(all_links))


all_messages = []

for link in all_links:
    driver.get(link)
    dict = {}
    dict['from'] = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//td/span[@class='val'][1]"))).text
    dict['date'] = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='m-header mh-DateUTS']/span[@class='val']"))).text
    dict['subject'] = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@id='msgFieldSubject']/span[@class='val']"))).text
    dict['message'] = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@id='viewmessagebody_BODY']"))).text
    all_messages.append(dict)

#pprint(all_messages)


mail_data.insert_many(all_messages)

driver.quit()