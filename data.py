import requests

base_url = "http://localhost:5000/"

user_data = {"username": "rodrigo", "password": "rodrigo"}
sent_data = {"name": "Reinhart", "race": "Humano", "class_": "Mosqueteiro", "level": "2"}

response = requests.post(base_url + "users", json=user_data)
# response = requests.post(base_url + "login", json=user_data)
# response = requests.post(base_url + "characters", json=sent_data, headers={"Authorization": f"Bearer {token_rodrigo}"})
# response = requests.get(base_url + "characters/3", headers={"Authorization": f"Bearer {token_rodrigo}"})
# response = requests.put(base_url + "characters/3", json={"name": "Urin-Kal"}, headers={"Authorization": f"Bearer {token_rodrigo}"})
# response = requests.delete(base_url + "characters/2", headers={"Authorization": f"Bearer {token_cayo}"})

print(f"Status code: {response.status_code}\nResponse: {response.text}")

# coisas a fazer: consertar o UTF, validar as entradas dos campos (ex. level só pode ser int), fazer o level ser opcional (ter 1 como valor default)
