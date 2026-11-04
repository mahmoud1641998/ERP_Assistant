from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

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

## Database health check endpoint
@router.get("/database")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }