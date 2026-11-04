from pydantic import BaseModel, Field


class ConversationAssistantRequest(BaseModel):

    question: str = Field(
        min_length=3,
        max_length=1000,
        description="Natural language question"
    )

    conversation_id: int | None = Field(
        default=None,
        description="Existing conversation ID. If omitted, a new conversation will be created."
    )


class ConversationAssistantResponse(BaseModel):

    success: bool

    conversation_id: int

    question: str

    sql: str | None = None

    model: str | None = None

    message: str

    row_count: int = 0

    data: list[dict] = Field(default_factory=list)

    answer: str | None = None