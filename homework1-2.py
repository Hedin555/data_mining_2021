import requests
import json

url = 'https://api.nasa.gov/DONKI/GST'
params = {'startDate': '2021-01-01', 'endDate': '2021-05-09', 'api_key': 'DEMO_KEY'}

response = requests.get(url, params=params).json()

for i in response:
    print(f"Cсылка на информацию по геомагнитной буре {i['startTime']}\n {i['link']}")

with open('GST.json', 'w') as f:
    json.dump(response, f)
