import requests
import json

# Имя пользователя github
username = "ubuntu"

# Запрос
repos = requests.get(f'https://api.github.com/users/{username}/repos')

# Выгружаем данные запроса в файл
with open('repo.json', 'w') as json_file:
    json.dump(repos.json(), json_file)

# Выводим в консоль репозитории
for repo in repos.json():
    if not repo['private']:
        print(repo['name'])
