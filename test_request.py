import requests

url = 'http://127.0.0.1:5027/api/token'
headers = {'Content-Type': 'application/json'}
data = {
    'email': 'admin@example.com',
    'password': 'password'
}

response = requests.post('http://127.0.0.1:5027/api/token', json={
    'email': 'admin@example.com',
    'password': 'password'
})


if response.status_code == 200:
    token = response.json().get('access_token')
else:
    print(f"Failed to get token: {response.status_code} - {response.text}")


# access_protected_endpoint(token):
url = 'http://127.0.0.1:5027/api/hello'

response = requests.get(url, headers={
    'Authorization': f'Bearer {token}'
})

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to access protected endpoint: {response.status_code} - {response.text}")
