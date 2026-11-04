# firs - test
from fastapi import FastAPI

app = FastAPI(
    title="ERP AI Assistant",
    description="Local AI-powered SQL Assistant for ERP Systems",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to ERP AI Assistant",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "ERP AI Assistant"
    }

# end of file