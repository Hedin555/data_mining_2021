from pymongo import MongoClient
from pprint import pprint
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup as bs
import hashlib

client = MongoClient('Localhost', 27017)

db = client['hhdb']

hh_vacancy = db.hh_vacancy


url = 'https://hh.ru/search/vacancy'
search = input('Введите слово для поиска: ')
params = {'text': search,
          'page': 0}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

response = requests.get(url, params=params, headers=headers)
dom = bs(response.text, 'html.parser')
page = int(dom.find_all('a', {'class': 'bloko-button'})[-2].getText())

vacancy = []

for p in range(0, page):
    params['page'] = p
    response = requests.get(url, params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})
    for vac in vacancy_list:
        vacancy_data = {}
        vacancy_name = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
        vacancy_link = vac.find('a', {'class': 'bloko-link'})['href']
        salary = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = salary.getText().replace(u'\u202F', u'')
            salary = re.split(r'\s|–', salary)
            salary_list = []
            for i in salary:
                if i != '':
                    salary_list.append(i)
            if salary_list[0] == 'до':
                salary_min = None
                salary_max = int(salary_list[1])
            elif salary_list[0] == 'от':
                salary_min = int(salary_list[1])
                salary_max = None
            else:
                salary_min = int(salary_list[0])
                salary_max = int(salary_list[1])

            salary_currency = salary_list[2]

#        encoded = hashlib.sha1((vacancy_link + vacancy_link).encode('utf-8'))
#        vacancy_data['_id'] = encoded.hexdigest()
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency

        vacancy.append(vacancy_data)


#Заполнение базы данных
def insert_mongodb():
    hh_vacancy.insert_many(vacancy)

#Отбор по зарлате
for hh_vacancy in hh_vacancy.find({'$or':[{'salary_min': {'$gt': 300000}}, {'salary_max': {'$gt': 300000}}]}):
    pprint(hh_vacancy)

