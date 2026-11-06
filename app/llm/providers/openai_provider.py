
from app.core.config import settings

from app.llm.providers.openai_compatible_provider import (
    OpenAICompatibleProvider
)


class OpenAIProvider(OpenAICompatibleProvider):

    def __init__(self):

        super().__init__(
            provider_name="openai",
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            model=settings.OPENAI_MODEL
        )
