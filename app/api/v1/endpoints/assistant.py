from fastapi import APIRouter, HTTPException

from app.schemas.sql import (
    SQLAssistantRequest,
    SQLAssistantResponse
)

from app.services.sql_assistant_service import SQLAssistantService


router = APIRouter()

sql_assistant_service = SQLAssistantService()


@router.post(
    "/ask",
    response_model=SQLAssistantResponse
)
def ask_assistant(request: SQLAssistantRequest):

    try:
        result = sql_assistant_service.ask(
            request.question
        )

        return SQLAssistantResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Assistant request failed: {str(e)}"
        )
    