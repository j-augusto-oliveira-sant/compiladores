import requests

codigo = """while ( x < 10 ) {
        x = 10 + 1
    }"""

data = {
    "codigo": codigo,
}

response = requests.post("http://127.0.0.1:8000/analise-lexica", data=data)
if response.status_code == 200:
    response_data = response.json()
    print(response_data)
else:
    print(response.status_code, response.text)
