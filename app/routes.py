from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from app.github_utils import clone_repo
from app.file_generator import generate_project_descriptor
from app.commit_dockerfile import commit_and_push_dockerfile
from app.dockerfile_generator import generate_dockerfile

router = APIRouter()

@router.post("/submit")
def submit_repo(repo_url: str = Form(...), github_token: str = Form(None)):
    try:
        path, clone_url = clone_repo(repo_url.strip(), github_token)
        descriptor = generate_project_descriptor(path)
        dockerfile_path = generate_dockerfile(descriptor, path)
        commit_and_push_dockerfile(path)

        return {
            "message": "Dockerfile generated and pushed ✅",
            "repo_path": path,
            "descriptor": descriptor,
            "dockerfile": dockerfile_path
        }

    except Exception as e:
        return {"error": str(e)}