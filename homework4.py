from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('Localhost', 27017)
db = client['news']
news_data = db.news_data
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

all_news = []

response_mail = requests.get('https://news.mail.ru', headers=headers)
dom_mail = html.fromstring(response_mail.text)

news_link_mail = dom_mail.xpath(".//a[@class='list__text']/@href")

for link in news_link_mail:
    news_mail = {}
    responce_news = requests.get(link, headers=headers)
    dom_news_mail = html.fromstring(responce_news.text)
    news_mail['source'] = dom_news_mail.xpath("//a[@class='link color_gray breadcrumbs__link']/@href")[0]
    news_mail['name'] = dom_news_mail.xpath("//h1[@class='hdr__inner']/text()")[0]
    news_mail['link'] = link
    news_mail['date'] = dom_news_mail.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0].split(r'T')[0]

    all_news.append(news_mail)


response_lenta = requests.get('https://lenta.ru/', headers=headers)
dom_lenta = html.fromstring(response_lenta.text)



news_link_lenta = dom_lenta.xpath("//section/div[contains(@class, 'b-yellow-box__wrap')]/div[contains(@class, 'item')]/a")

for link in news_link_lenta:
    news_lenta = {}
    news_lenta['source'] = 'https://lenta.ru/'
    news_lenta['name'] = link.xpath('.//text()')[0].replace('\xa0', ' ')
    news_lenta['link'] = 'https://lenta.ru' + link.xpath('.//@href')[0]
    responce_news = requests.get(news_lenta['link'], headers=headers)
    dom_lnews = html.fromstring(responce_news.text)
    news_lenta['date'] = dom_lnews.xpath("//div[contains(@class, 'topic__info')]/time/@datetime")[0].split(r'T')[0]

    all_news.append(news_lenta)


news_data.insert_many(all_news)
pprint(all_news)
