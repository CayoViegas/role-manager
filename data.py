import requests

base_url = "http://localhost:5000/"

sent_data = {"name": "Okayu", "race": "Humano", "class_": "Guerreiro", "level": 3}

# response = requests.post(base_url + "characters", json=sent_data)
response = requests.get(base_url + "characters/3")
# response = requests.put(base_url + "characters/3", json={"name": "Korone"})
# response = requests.delete(base_url + "characters/2")

print(f"Status code: {response.status_code}\nResponse: {response.json()['name']}")
