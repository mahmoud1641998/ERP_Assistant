from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    models,
    schema,
    sql,
    assistant,
    conversations
)


api_router = APIRouter()


api_router.include_router(
    health.router,
    tags=["System"]
)

api_router.include_router(
    models.router,
    prefix="/api/v1",
    tags=["Ollama"]
)

api_router.include_router(
    schema.router,
    prefix="/api/v1",
    tags=["Database Schema"]
)

api_router.include_router(
    sql.router,
    prefix="/api/v1/sql",
    tags=["SQL Generation"]
)

api_router.include_router(
    assistant.router,
    prefix="/api/v1/assistant",
    tags=["Assistant"]
)

api_router.include_router(
    conversations.router,
    prefix="/api/v1/conversations",
    tags=["Conversations"]
)