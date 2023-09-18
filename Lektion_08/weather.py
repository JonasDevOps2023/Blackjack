import requests
import json

url = 'https://54qhf521ze.execute-api.eu-north-1.amazonaws.com/weather/stockholm'
response = requests.get(url)

response_dictionary = json.loads(response.text)
print(response_dictionary)