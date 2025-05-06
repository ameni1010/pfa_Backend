from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from app.github_action_generator import generate_github_action
from app.github_utils import clone_repo
from app.file_generator import generate_project_descriptor
from app.commit_dockerfile import commit_and_push_files
from app.dockerfile_generator import generate_dockerfile
from app.k8s_generator import generate_k8s_manifests
import os

router = APIRouter()
def extract_github_username(repo_url: str) -> str:
    parts = repo_url.strip().rstrip("/").split("/")
    if len(parts) >= 2:
        return parts[-2]  # username is just before the repo name
    return "unknown"
@router.post("/submit")
def submit_repo(repo_url: str = Form(...), github_token: str = Form(None)):
    try:
        path, clone_url = clone_repo(repo_url.strip(), github_token)
        descriptor = generate_project_descriptor(path)
        dockerfile_path = generate_dockerfile(descriptor, path)
        github_username = extract_github_username(repo_url)
        workflow_path = generate_github_action(
            repo_path=path,
            dockerhub_username="ameni1010",
            github_username=github_username,
            language=descriptor["language"]
        )
        image_tag = "sha-" + descriptor["git_sha"]
        app_name = os.path.basename(path.rstrip("/\\"))
        port = descriptor.get("port", 5000)
        k8s_output_dir = os.path.join(path, "k8s")
        k8s_files = generate_k8s_manifests(app_name, port, image_tag, k8s_output_dir)

        push_result = commit_and_push_files(path, [dockerfile_path, workflow_path])

        return {
            "message": push_result,
            "repo_path": path,
            "descriptor": descriptor,
            "dockerfile": dockerfile_path, 
            "workflow": workflow_path, 
            "k8s_files": k8s_files

        }

    except Exception as e:
        return {"error": str(e)}