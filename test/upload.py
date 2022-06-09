import requests

fish = open("asagi.jpg", "rb")
url = 'http://127.0.0.1:8080/predict'
res = requests.post(url, files={"file": fish})
print(res.text)