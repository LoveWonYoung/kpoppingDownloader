import requests


u = "https://kpopping.com"+'/kpics/240519-WONYOUNG-LEESEO-FANSIGN-EVENT'

res = requests.post(u)

print(res.text)