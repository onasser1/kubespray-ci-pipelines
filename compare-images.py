import os
import requests

url = "https://quay.io/api/v1/repository"

def get_all_quay_repos(namespace):
    all_repos = []
    next_page = None
    
    while True:
        params = {
            'namespace': namespace,
            'public': 'true'
        }
        if next_page:
            params['next_page'] = next_page

        response = requests.get(url, params=params)
        data = response.json()

        for repo in data.get('repositories', []):
            if repo['name'].startswith("vm-"):
                all_repos.extend([repo['name'].removeprefix('vm-')])

        next_page = data.get('next_page')
        
        if not next_page:
            break
    return all_repos

repos_list = get_all_quay_repos("kubespray")
removed_repos = []
raw_env = os.getenv("LATEST_RELEASES", "")
active_branches = raw_env.split()

for repo in repos_list:
    count = 0
    for ab in active_branches:
        response = requests.get(f"https://raw.githubusercontent.com/kubernetes-sigs/kubespray/{ab}/test-infra/image-builder/roles/kubevirt-images/defaults/main.yml")
        if repo not in response.text:
            count = count + 1
            if count == len(active_branches):
                removed_repos.append(repo)
            continue

with open("build.env", "w") as f:
    repos_string = " ".join(removed_repos)
    f.write(f'REPOS_TO_DELETE="{repos_string}"\n')