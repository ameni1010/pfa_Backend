from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Auto-Deployer",
    description="Automatically deploy apps from GitHub to Kubernetes",
    version="1.0.0"
)

app.include_router(router)
