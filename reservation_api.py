import requests

url = "https://hapio.io/"
api_key = "nInGijy7nRev240ONpV0ptmubnDoANC4mcYPtyGh96848012"

headers = {"Authorisation" : f"Barear {api_key}",
           "Content-Type" : "Bookings/json"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
