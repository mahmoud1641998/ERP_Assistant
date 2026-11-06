
from app.core.config import settings

from app.llm.providers.openai_compatible_provider import (
    OpenAICompatibleProvider
)


class KimiProvider(OpenAICompatibleProvider):

    def __init__(self):

        super().__init__(
            provider_name="kimi",
            api_key=settings.KIMI_API_KEY,
            base_url=settings.KIMI_BASE_URL,
            model=settings.KIMI_MODEL
        )
