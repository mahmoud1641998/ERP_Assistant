from app.core.config import settings

from app.llm.base import BaseLLMProvider
from app.llm.providers.ollama_provider import OllamaProvider
from app.llm.providers.openai_provider import OpenAIProvider
from app.llm.providers.kimi_provider import KimiProvider


class LLMFactory:

    @staticmethod
    def get_provider() -> BaseLLMProvider:

        provider_name = settings.LLM_PROVIDER.strip().lower()

        if provider_name == "ollama":
            return OllamaProvider()

        if provider_name == "openai":
            return OpenAIProvider()

        if provider_name == "kimi":
            return KimiProvider()

        raise ValueError(
            f"Unsupported LLM provider: {provider_name}"
        )