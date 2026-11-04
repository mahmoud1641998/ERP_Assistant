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
        # Step 1: Run the Assistant workflow
        result = sql_assistant_service.ask(
            request.question
        )

        # Step 2: Handle known errors
        if not result["success"]:

            error_type = result.get("error_type")

            error_detail = {
                "error_type": error_type,
                "message": result["message"]
            }

            if error_type == "validation_error":
                raise HTTPException(
                    status_code=422,
                    detail=error_detail
                )

            elif error_type == "execution_error":
                raise HTTPException(
                    status_code=500,
                    detail=error_detail
                )

            elif error_type == "answer_generation_error":
                return SQLAssistantResponse(**result)

        # Step 3: Return successful response
        return SQLAssistantResponse(**result)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Assistant request failed."
        )