from sqlalchemy.orm import Session

from app.models import Conversation, ConversationMessage


class ConversationService:

    def create_conversation(
        self,
        db: Session,
        title: str | None = None
    ):

        conversation = Conversation(
            title=title
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def add_message(
        self,
        db: Session,
        conversation_id: int,
        role: str,
        content: str
    ):

        message = ConversationMessage(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def get_conversation(
        self,
        db: Session,
        conversation_id: int
    ):

        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        return conversation

    def get_messages(
        self,
        db: Session,
        conversation_id: int
    ):

        messages = db.query(ConversationMessage).filter(
            ConversationMessage.conversation_id == conversation_id
        ).order_by(
            ConversationMessage.created_at.asc()
        ).all()

        return messages