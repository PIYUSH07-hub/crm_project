import requests

url = "http://127.0.0.1:8000/api/clients/"
headers = {
    "Authorization": "Token 4ae1e34d80997d99257d8460fdc88bb6cd35706b"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())





# {
#   "username": "Piyush004",
#   "password": "a-,C&~YXZJ=GC2Z"
# }

# {
#   "username": "Piyush",
#   "password": "Piyush"
# }