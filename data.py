import requests

base_url = "http://localhost:5000/"

user_data = {"username": "cayo", "password": "galaseca17"}
sent_data = {"name": "Úrin-Kal", "race": "Aasimar", "class_": "Paladino", "level": 3}

token_rodrigo = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNzI2NjMxNjEzfQ.XBt_skYC_kTwagcflz3sy2VEtBUhsrCifCVR0KGDqmA"
token_cayo = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzI2NjMxNzIyfQ.uUG4uAf9jsBsQMfsLe7NB6eUStZY7OE1sbEtYj9_dwA"

# response = requests.post(base_url + "users", json=user_data)
# response = requests.post(base_url + "login", json=user_data)
# response = requests.post(base_url + "characters", json=sent_data, headers={"Authorization": f"Bearer {token_rodrigo}"})
response = requests.get(base_url + "characters", headers={"Authorization": f"Bearer {token_cayo}"})
# response = requests.put(base_url + "characters/2", json={"level": 3}, headers={"Authorization": f"Bearer {token_rodrigo}"})
# response = requests.delete(base_url + "characters/3", headers={"Authorization": f"Bearer {token_rodrigo}"})
# response = requests.delete(base_url + "users/1", headers={"Authorization": f"Bearer {token_rodrigo}"})

print(f"Status code: {response.status_code}\nResponse: {response.text}")

# coisas a fazer: consertar o UTF, validar as entradas dos campos (ex. level só pode ser int), fazer o level ser opcional (ter 1 como valor default)
