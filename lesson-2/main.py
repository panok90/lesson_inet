import requests
from bs4 import BeautifulSoup

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
for item in base_list:
    wage = []
    a_tag = item.find('span', {'class': 'g-user-content'})
    name = a_tag.getText()
    link = list(a_tag.children)[0].get('href')

    print()
