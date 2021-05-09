import requests
from pprint import pprint
import json

url = 'https://api.github.com'
username = 'Hedin555'

response = requests.get(f'{url}/users/{username}/repos').json()

for i in response:
    print(i['name'])

with open('data.json', 'w') as f:
    json.dump(response, f)
