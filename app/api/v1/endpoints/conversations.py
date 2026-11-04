from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas import (
    ConversationCreate,
    ConversationResponse,
    ConversationMessageCreate,
    ConversationMessageResponse
)

from app.services.conversation_service import ConversationService


router = APIRouter()

conversation_service = ConversationService()


@router.post(
    "/",
    response_model=ConversationResponse
)
def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db)
):

    conversation = conversation_service.create_conversation(
        db=db,
        title=request.title
    )

    return conversation


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):

    conversation = conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    return conversation


@router.get(
    "/{conversation_id}/messages",
    response_model=list[ConversationMessageResponse]
)
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):

    conversation = conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    messages = conversation_service.get_messages(
        db=db,
        conversation_id=conversation_id
    )

    return messages


@router.post(
    "/{conversation_id}/messages",
    response_model=ConversationMessageResponse
)
def add_conversation_message(
    conversation_id: int,
    request: ConversationMessageCreate,
    db: Session = Depends(get_db)
):

    conversation = conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    message = conversation_service.add_message(
        db=db,
        conversation_id=conversation_id,
        role=request.role,
        content=request.content
    )

    return message