import os
import requests

def get_all_quay_repos(namespace):
    all_repos = []
    next_page = None
    url = "https://quay.io/api/v1/repository"
    
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
active_branches = ['master', 'release-2.30', 'release-2.29', 'release-2.28', 'release-2.27', 'release-2.26']

for repo in repos_list:
    count = 0
    for ab in active_branches:
        response = requests.get(f"https://raw.githubusercontent.com/kubernetes-sigs/kubespray/{ab}/test-infra/image-builder/roles/kubevirt-images/defaults/main.yml")
        if repo not in response.text:
            #print(f"{repo} from quay.io is not in release branch: {ab}")
            count = count + 1
            if count == len(active_branches):
                #print(f"================================\nThis image should be deleted from quay.io registry: {repo}, because it's not used in any active release branch.")
                removed_repos.append(repo)
            continue

print(removed_repos)