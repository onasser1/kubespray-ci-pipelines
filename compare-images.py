import os
import requests

response = requests.get("https://quay.io/api/v1/repository?namespace=kubespray&public=true")
data = response.json()
quay_repos = [repo["name"] for repo in data.get("repositories", [])]

print(quay_repos)