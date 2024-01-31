import requests

url = "https://eu-central-1.hapio.net/"
api_key = "nInGijy7nRev240ONpV0ptmubnDoANC4mcYPtyGh96848012"

headers = {"Authorization" : f"Barear {api_key}",
           "Content-Type" : "application/json"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
