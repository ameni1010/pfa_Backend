import os
import json

def generate_project_descriptor(repo_path: str) -> dict:
    descriptor = {
        "language": "unknown",
        "dependency_file": None,
        "run_command": None,
        "build_command": None,
        "port": None,
        "detected_by": []
    }

    all_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            filepath = os.path.join(root, file)
            all_files.append((file, filepath))

    # === PYTHON DETECTION ===
    py_entry = None
    for name, path in all_files:
        if name == "requirements.txt":
            descriptor["language"] = "python"
            descriptor["dependency_file"] = path
            descriptor["build_command"] = "pip install -r requirements.txt"
            descriptor["port"] = 5000
            if name not in descriptor["detected_by"]:
                descriptor["detected_by"].append(name)
        if name in ["app.py", "main.py"]:
            py_entry = path
            descriptor["run_command"] = f"python {name}"
            if name not in descriptor["detected_by"]:
                descriptor["detected_by"].append(name)

    if descriptor["language"] == "python" and not descriptor["run_command"]:
        descriptor["run_command"] = "python app.py"

    # === NODE.JS DETECTION ===
    for name, path in all_files:
        if name == "package.json":
            descriptor["language"] = "nodejs"
            descriptor["dependency_file"] = path
            descriptor["build_command"] = "npm install"
            descriptor["run_command"] = "npm start"
            descriptor["port"] = 3000
            if name not in descriptor["detected_by"]:
                descriptor["detected_by"].append(name)
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    if "scripts" in data and "start" in data["scripts"]:
                        descriptor["run_command"] = "npm start"
                    elif "main" in data:
                        descriptor["run_command"] = f"node {data['main']}"
            except Exception as e:
                print(f"Error reading package.json: {e}")
            break

    # === JAVA DETECTION ===
    for name, path in all_files:
        if name == "pom.xml":
            descriptor["language"] = "java"
            descriptor["dependency_file"] = path
            descriptor["build_command"] = "mvn package"
            descriptor["run_command"] = "java -jar target/*.jar"
            descriptor["port"] = 8080
            if name not in descriptor["detected_by"]:
                descriptor["detected_by"].append(name)
            break

    # === PHP DETECTION ===
    for name, path in all_files:
        if name == "composer.json":
            descriptor["language"] = "php"
            descriptor["dependency_file"] = path
            descriptor["build_command"] = "composer install"
            descriptor["run_command"] = "php -S 0.0.0.0:80 -t public"
            descriptor["port"] = 80
            if name not in descriptor["detected_by"]:
                descriptor["detected_by"].append(name)
            break

    # === GO DETECTION ===
    for name, path in all_files:
        if name == "go.mod":
            descriptor["language"] = "go"
            descriptor["dependency_file"] = path
            descriptor["build_command"] = "go build -o main ."
            descriptor["run_command"] = "./main"
            descriptor["port"] = 8080
            if name not in descriptor["detected_by"]:
                descriptor["detected_by"].append(name)
            break

    return descriptor
