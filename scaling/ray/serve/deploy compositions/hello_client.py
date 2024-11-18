import requests

response = requests.post(
    "http://localhost:8000", json={"language": "spanish", "name": "Dora"}
)
greeting = response.text
print(greeting)