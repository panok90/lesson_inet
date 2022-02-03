import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from pprint import pprint


def find_wage(elem, collection):
    find_list = list(collection.find({'$or': [{'min': {'$gt': elem}}, {'max': {'$gt': elem}}]}))
    pprint(find_list)


job = 'python'
# Параметры запроса
params = dict()
params['clusters'] = 'true'
params['area'] = '1'
params['ored_clusters'] = 'true'
params['enable_snippets'] = 'true'
params['text'] = job

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

# Запрос
response = requests.get(f'https://hh.ru/search/vacancy', params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

base_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

result = []
for item in base_list:
    item_result = dict()
    # wage_list = {'min': None, 'max': None, 'currency': None}
    a_tag = item.find('span', {'class': 'g-user-content'})
    item_result['name'] = a_tag.getText()
    item_result['link'] = list(a_tag.children)[0].get('href')
    let_list = ['от', 'до']
    try:
        str_wage = str(item.find('span', attrs={'class': 'bloko-header-section-3',
                                                'data-qa': 'vacancy-serp__vacancy-compensation'}).getText())
        params_wage = str_wage.split()
        item_result['currency'] = params_wage[-1]
        params_wage = params_wage[:-1]
        if params_wage[0] in let_list:
            int_wage = int(params_wage[1] + params_wage[2])
            if params_wage[0] == let_list[0]:
                item_result['min'] = int_wage
            else:
                item_result['max'] = int_wage
        else:
            int_wage_min = int(params_wage[0] + params_wage[1])
            item_result['min'] = int_wage_min
            int_wage_max = int(params_wage[3] + params_wage[4])
            item_result['max'] = int_wage_max
    except:
        item_result['currency'] = None
        item_result['min'] = None
        item_result['max'] = None
    item_result['site'] = 'hh.ru'
    result.append(item_result)

client = MongoClient('127.0.0.1', 27017)
db = client['database']
# db.jobs.drop()
jobs = db.jobs

for doc in result:
    if jobs.find_one({'link': doc['link']}):
        continue
    jobs.insert_one(doc)

wage = 200000
find_wage(wage, jobs)
