from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Conversation(Base):

    __tablename__ = "ai_conversations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    messages: Mapped[list["ConversationMessage"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan"
    )
# اول اضافه لقاعدة البيانات لو لم يكن موجود
# from app.core.database import engine
# from app.models.base import Base
# from app.models import Conversation

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