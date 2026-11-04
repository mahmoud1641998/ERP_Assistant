from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ConversationMessage(Base):

    __tablename__ = "ai_conversation_messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    conversation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ai_conversations.id"),
        nullable=False,
        index=True
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages"
    )

    # ده لو الجدول مش موجود هينشأه

    # from app.core.database import engine
    # from app.models.base import Base
    # from app.models import Conversation, ConversationMessage


    # Base.metadata.create_all(bind=engine)

    # print("Tables created successfully.")
    # -----------------------------------------

    # ده بيتأكد إن SQLAlchemy شايف الجدولين قبل ما نطلب منه إنشاءهم في MySQL.
    # from app.models.base import Base
    # from app.models import Conversation, ConversationMessage


    # print("Registered Tables:")
    # print(Base.metadata.tables.keys())

    # print("\nConversation Model:")
    # print(Conversation.__tablename__)

    # print("\nConversation Message Model:")
    # print(ConversationMessage.__tablename__)