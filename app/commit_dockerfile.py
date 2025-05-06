import git
import os

def commit_and_push_files(repo_path: str, files_to_commit: list):
    try:
        repo = git.Repo(repo_path)

        for file in files_to_commit:
            # Make path relative to repo root
            rel_path = os.path.relpath(file, repo_path)
            repo.git.add(rel_path)

        if repo.is_dirty(untracked_files=True):
            repo.git.commit("-m", "Auto-generated Dockerfile and GitHub Actions workflow")
            repo.git.push()
            return "Files committed and pushed ✅"
        else:
            return "No changes to commit — already up to date ✅"

    except Exception as e:
        raise RuntimeError(f"Failed to push files: {e}")
