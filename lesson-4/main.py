import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint

# Параметры запроса
source = 'https://news.mail.ru'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

# Запрос
response = requests.get(source, headers=headers)

dom = html.fromstring(response.text)

table_news = dom.xpath("//div[contains(@class, 'daynews__item')]/a/@href")
links_news = dom.xpath("//ul[@class='list list_type_square list_half js-module']/li[@class='list__item']/a/@href")
links = table_news + links_news
client = MongoClient('127.0.0.1', 27017)
db = client['database']
# db.jobs.drop()
news = db.news
for link in links:
    new = dict()
    current_response = requests.get(link, headers=headers)
    current_dom = html.fromstring(current_response.text)
    new['source'] = source
    new['link'] = link
    new['name'] = current_dom.xpath("//h1//text()")[0]
    date = current_dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
    new['date'] = date.split('T')[0]
    if news.find_one({'link': new['link']}):
        continue
    news.insert_one(new)

pprint(list(news.find({})))
