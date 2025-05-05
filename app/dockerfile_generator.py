import os

def generate_dockerfile(descriptor: dict, repo_path: str) -> str:
    language = descriptor.get("language")
    dockerfile_path = os.path.join(repo_path, "Dockerfile")

    if language == "python":
        base_image = "python:3.10"
    elif language == "nodejs":
        base_image = "node:18"
    elif language == "java":
        base_image = "openjdk:17"
    elif language == "php":
        base_image = "php:8.1-apache"
    elif language == "go":
        base_image = "golang:1.21"
    else:
        raise ValueError("Unsupported or unknown language")

    # Build the Dockerfile lines
    lines = [
        f"FROM {base_image}",
        "WORKDIR /app",
        "COPY . ."
    ]

    if descriptor.get("build_command"):
        lines.append(f"RUN {descriptor['build_command']}")

    if descriptor.get("port"):
        lines.append(f"EXPOSE {descriptor['port']}")

    if descriptor.get("run_command"):
        # Convert run_command string into CMD array format
        cmd_list = descriptor['run_command'].split()
        lines.append(f'CMD {cmd_list!r}')  # e.g. CMD ['python', 'app.py']

    # Write to file
    with open(dockerfile_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    return dockerfile_path
