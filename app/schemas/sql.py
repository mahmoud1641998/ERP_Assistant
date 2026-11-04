from pydantic import BaseModel, Field


class SQLGenerationRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000,
        description="Natural language question"
    )


class SQLGenerationResponse(BaseModel):
    success: bool
    question: str
    sql: str | None = None
    model: str | None = None
    message: str

class SQLAssistantRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000,
        description="Natural language question"
    )


class SQLAssistantResponse(BaseModel):
    success: bool
    question: str
    generated_sql: str | None = None
    message: str
    row_count: int = 0
    data: list[dict] = []
    answer: str | None = None
    model: str | None = None