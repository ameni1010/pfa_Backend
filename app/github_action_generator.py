import os

def generate_github_action(repo_path: str, dockerhub_username: str, github_username: str, language: str) -> str:
    repo_name = os.path.basename(repo_path.rstrip("/\\"))
    image_base = f"{dockerhub_username}/{github_username}-{repo_name}"

    workflows_dir = os.path.join(repo_path, ".github", "workflows")
    os.makedirs(workflows_dir, exist_ok=True)

    # Optional test/lint blocks
    test_block = ""
    lint_block = ""

    if language == "python":
        test_block = """
    - name: Run Python tests
      continue-on-error: true
      run: |
        pip install pytest
        pytest
"""
        lint_block = """
    - name: Run Python linter (non-blocking)
      continue-on-error: true
      run: |
        pip install flake8
        flake8 .
"""
    elif language == "nodejs":
        test_block = """
    - name: Run Node.js tests
      run: npm test
"""
        lint_block = """
    - name: Run ESLint
      run: |
        npm install
        npx eslint .
"""

    content = f"""
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
    paths:
      - Dockerfile
      - '**/*.py'
      - '**/*.js'
      - '.github/workflows/docker.yml'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Generate tags
      id: vars
      run: |
        echo "timestamp=$(date +'%Y%m%d-%H%M')" >> $GITHUB_ENV
        echo "sha_short=$(echo ${{{{ github.sha }}}} | cut -c1-7)" >> $GITHUB_ENV

    - name: Log in to DockerHub
      run: echo "${{{{ secrets.DOCKER_PASSWORD }}}}" | docker login -u "${{{{ secrets.DOCKER_USERNAME }}}}" --password-stdin

    {lint_block.strip()}

    {test_block.strip()}

    - name: Build Docker image
      run: |
        docker build -t {image_base}:latest .
        docker tag {image_base}:latest {image_base}:${{{{ env.timestamp }}}}
        docker tag {image_base}:latest {image_base}:sha-${{{{ env.sha_short }}}}

    - name: Push Docker images
      run: |
        docker push {image_base}:latest
        docker push {image_base}:${{{{ env.timestamp }}}}
        docker push {image_base}:sha-${{{{ env.sha_short }}}}
"""

    workflow_path = os.path.join(workflows_dir, "docker.yml")
    with open(workflow_path, "w") as f:
        f.write(content.strip() + "\n")

    return workflow_path
