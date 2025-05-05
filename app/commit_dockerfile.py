import git

def commit_and_push_dockerfile(repo_path: str):
    try:
        repo = git.Repo(repo_path)
        repo.git.add("Dockerfile")
        repo.git.commit("-m", "Auto-generated Dockerfile")
        repo.git.push()
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to push Dockerfile: {e}")
