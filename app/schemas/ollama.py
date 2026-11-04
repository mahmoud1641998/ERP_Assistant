from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(
        min_length=1,
        description="The user prompt"
    )

    model: str = Field(
        default="qwen3:4b-instruct-2507-q4_K_M",
        description="Ollama model name"
    )