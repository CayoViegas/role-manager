import requests

base_url = "http://localhost:5000/"

user_data = {"username": "rodrigo", "password": "galaseca17"}
sent_data = {"name": "Okayu", "race": "Humano", "class_": "Guerreiro", "level": 2}

token_rodrigo = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzI2NjE1NzM1fQ.YZH2Ay6UFPk571_zHrWurWEXt2jSeZpbfU8tjKifQ4k"

# response = requests.post(base_url + "users", json=user_data)
# response = requests.post(base_url + "login", json=user_data)
# response = requests.post(base_url + "characters", json=sent_data, headers={"Authorization": f"Bearer {token_rodrigo}"})
# response = requests.get(base_url + "characters", headers={"Authorization": f"Bearer {token_rodrigo}"})
# response = requests.put(base_url + "characters/2", json={"level": 3}, headers={"Authorization": f"Bearer {token_rodrigo}"})
# response = requests.delete(base_url + "characters/3", headers={"Authorization": f"Bearer {token_rodrigo}"})
response = requests.delete(base_url + "users/1", headers={"Authorization": f"Bearer {token_rodrigo}"})

print(f"Status code: {response.status_code}\nResponse: {response.text}")

# coisas a fazer: consertar o UTF, validar as entradas dos campos (ex. level só pode ser int), fazer o level ser opcional (ter 1 como valor default)
