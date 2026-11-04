from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to ERP AI Assistant",
        "status": "running"
    }


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "ERP AI Assistant"
    }