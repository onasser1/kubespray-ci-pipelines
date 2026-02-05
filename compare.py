import os
import requests

# ... (keep your get_all_quay_repos function as is) ...

repos_list = get_all_quay_repos("kubespray")
active_branches = ['master', 'release-2.30', 'release-2.29', 'release-2.28', 'release-2.27', 'release-2.26']
removed_repos = []

# 1. PRE-FETCH: Download all branch files once and store in a dictionary
branch_data = {}
for ab in active_branches:
    url = f"https://raw.githubusercontent.com/kubernetes-sigs/kubespray/{ab}/test-infra/image-builder/roles/kubevirt-images/defaults/main.yml"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        branch_data[ab] = response.text
        print(f"Cached data for branch: {ab}")
    except Exception as e:
        print(f"Warning: Could not fetch {ab}: {e}")

# 2. LOCAL SEARCH: Compare repos against cached data (Fast!)
for repo in repos_list:
    unused_count = 0
    for ab, content in branch_data.items():
        if repo not in content:
            unused_count += 1
    
    # If the repo was not found in ANY of the cached branch files
    if unused_count == len(branch_data):
        removed_repos.append(repo)

# 3. EXPORT for GitLab CI
with open("build.env", "w") as f:
    f.write(f"REPOS_TO_DELETE={' '.join(removed_repos)}\n")

print(f"Analysis complete. Found {len(removed_repos)} repos to delete.")