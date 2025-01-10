import requests
try:
    response = requests.get("http://10.100.133.23:6006/v1/models")
    print("Server is reachable")
except requests.exceptions.ConnectionError:
    print("Cannot connect to server")