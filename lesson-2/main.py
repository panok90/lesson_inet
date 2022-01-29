import requests
from bs4 import BeautifulSoup
from pprint import pprint

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
    wage_list = [None] * 3
    a_tag = item.find('span', {'class': 'g-user-content'})
    item_result['name'] = a_tag.getText()
    item_result['link'] = list(a_tag.children)[0].get('href')
    let_list = ['от', 'до']
    try:
        wage = str(item.find('span', attrs={'class': 'bloko-header-section-3',
                                                       'data-qa': 'vacancy-serp__vacancy-compensation'}).getText())
        wage = wage.split()
        wage_list[2] = wage[-1]
        wage = wage[:-1]
        if wage[0] in let_list:
            int_wage = int(wage[1] + wage[2])
            if wage[0] == let_list[0]:
                wage_list[0] = int_wage
            else:
                wage_list[1] = int_wage
        else:
            int_wage_min = int(wage[0] + wage[1])
            wage_list[0] = int_wage_min
            int_wage_max = int(wage[3] + wage[4])
            wage_list[1] = int_wage_max

    except:
        wage_list = None
    item_result['wage'] = wage_list
    item_result['site'] = 'hh.ru'
    result.append(item_result)

pprint(result)