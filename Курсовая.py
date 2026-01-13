import requests
import os
import json

cat_says = input('Подпись к картинке с котом: ')
token = input('Введите токен для Яндекса: ')
group = 'pyqa-124'

with open(f'cats/{cat_says}.jpg', 'wb') as f:
    f.write(requests.get(f'https://cataas.com/cat/says/{cat_says}').content)

file_size = os.path.getsize(f'cats/{cat_says}.jpg')
data = {
    "file_name": f"{cat_says}.jpg",
    "file_size": file_size
}
with open(f"cats/{cat_says}.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

params = {'path': f'{group}'}
headers = {'Authorization': 'OAuth ' + token}
response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=headers, params=params)

params = {'path': f'{group}/{cat_says}'}
response1 = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers, params=params)

with open(f'cats/{cat_says}.jpg', 'rb') as f:
    requests.put(response1.json()['href'], files={'file': f})