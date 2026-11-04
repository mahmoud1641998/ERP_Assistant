from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="ERP AI Assistant",
    description="Local AI-powered SQL Assistant for ERP Systems",
    version="1.0.0"
)

app.include_router(api_router)