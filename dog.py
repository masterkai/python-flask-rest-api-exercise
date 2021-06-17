import requests
import json

url = "https://dog.ceo/api/breeds/image/random"

payload = 'name=my%20course'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': '__cfduid=da95575b9263b16d54c050fa22fe2c7221606996584'
}

response = requests.request("GET", url, headers=headers, data = payload)

data = json.loads(response.text)
print(data['message'])