import os
import re
import shutil
import git

def sanitize_repo_name(url: str) -> str:
    # Extract the repo name and strip invalid characters (like \n, :, etc.)
    repo_name = url.rstrip('/').split('/')[-1]
    return re.sub(r'[^\w.-]', '', repo_name)  # Only keep safe characters

def clone_repo(repo_url: str, token: str = None, base_dir="cloned_repos") -> tuple:
    repo_name = sanitize_repo_name(repo_url)
    repo_path = os.path.join(base_dir, repo_name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    os.makedirs(base_dir, exist_ok=True)

    if token:
        # inject token into clone URL
        repo_url_with_auth = repo_url.replace("https://", f"https://{token}@")
    else:
        repo_url_with_auth = repo_url

    git.Repo.clone_from(repo_url_with_auth, repo_path)
    return repo_path, repo_url_with_auth
