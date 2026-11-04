from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas import (
    ConversationAssistantRequest,
    ConversationAssistantResponse
)

from app.services.conversation_assistant_service import (
    ConversationAssistantService
)


router = APIRouter()

conversation_assistant_service = ConversationAssistantService()


@router.post(
    "/ask",
    response_model=ConversationAssistantResponse
)
def ask_conversation_assistant(
    request: ConversationAssistantRequest,
    db: Session = Depends(get_db)
):

    try:

        result = conversation_assistant_service.ask(
            db=db,
            user_question=request.question,
            conversation_id=request.conversation_id
        )

        if not result["success"]:

            if result["message"] == "Conversation not found.":

                raise HTTPException(
                    status_code=404,
                    detail=result["message"]
                )

            raise HTTPException(
                status_code=422,
                detail=result["message"]
            )

        return ConversationAssistantResponse(**result)

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Conversation assistant request failed."
        )