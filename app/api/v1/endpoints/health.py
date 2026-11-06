
from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import ai_engine, erp_engine


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


# Database health check endpoint
@router.get("/database")
def database_health():

    databases = {}

    # Check AI Assistant Database
    try:
        with ai_engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        databases["ai_assistant"] = "connected"

    except Exception:
        databases["ai_assistant"] = "disconnected"

    # Check ERP Database
    try:
        with erp_engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        databases["erp"] = "connected"

    except Exception:
        databases["erp"] = "disconnected"

    # Determine overall status
    overall_status = (
        "healthy"
        if all(status == "connected" for status in databases.values())
        else "unhealthy"
    )

    return {
        "status": overall_status,
        "application": "ERP AI Assistant",
        "databases": databases
    }
