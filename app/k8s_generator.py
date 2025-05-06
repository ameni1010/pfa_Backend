import os

def generate_k8s_manifests(app_name, port, image_tag, output_dir):
    deployment = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: ameni1010/{app_name}:{image_tag}
        ports:
        - containerPort: {port}
""".strip()

    service = f"""
apiVersion: v1
kind: Service
metadata:
  name: {app_name}
spec:
  selector:
    app: {app_name}
  ports:
    - protocol: TCP
      port: 80
      targetPort: {port}
  type: NodePort
""".strip()

    os.makedirs(output_dir, exist_ok=True)

    deployment_path = os.path.join(output_dir, "deployment.yaml")
    service_path = os.path.join(output_dir, "service.yaml")

    with open(deployment_path, "w") as f:
        f.write(deployment)

    with open(service_path, "w") as f:
        f.write(service)

    return [deployment_path, service_path]
