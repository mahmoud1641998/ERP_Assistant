
import ollama

from app.core.config import settings
from app.llm.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):

    def __init__(self):

        self.client = ollama.Client(
            host=settings.OLLAMA_BASE_URL,
            timeout=settings.LLM_TIMEOUT
        )

        self.model = settings.OLLAMA_MODEL

    def generate_response(
        self,
        prompt: str
    ) -> dict:

        try:

            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False,
                options={
                    "num_predict": settings.LLM_MAX_TOKENS,
                    "temperature": settings.LLM_TEMPERATURE
                }
            )

            return {
                "provider": "ollama",
                "model": self.model,
                "response": response.response
            }

        except Exception as e:

            raise Exception(
                f"Ollama generation failed: {str(e)}"
            )
