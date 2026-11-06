
import httpx

from app.core.config import settings
from app.llm.base import BaseLLMProvider


class OpenAICompatibleProvider(BaseLLMProvider):

    def __init__(
        self,
        provider_name: str,
        api_key: str,
        base_url: str,
        model: str
    ):

        self.provider_name = provider_name
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate_response(
        self,
        prompt: str
    ) -> dict:

        if not self.api_key:
            raise ValueError(
                f"{self.provider_name} API key is not configured."
            )

        if not self.model:
            raise ValueError(
                f"{self.provider_name} model is not configured."
            )

        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": settings.LLM_TEMPERATURE,
            "max_completion_tokens": settings.LLM_MAX_TOKENS
        }

        try:

            response = httpx.post(
                url,
                headers=headers,
                json=payload,
                timeout=settings.LLM_TIMEOUT
            )

            response.raise_for_status()

        except httpx.HTTPStatusError as e:

            raise RuntimeError(
                f"{self.provider_name} API returned status code: "
                f"{e.response.status_code}"
            ) from e

        except httpx.RequestError as e:

            raise RuntimeError(
                f"{self.provider_name} connection failed: {str(e)}"
            ) from e

        try:

            response_data = response.json()

        except ValueError as e:

            raise RuntimeError(
                f"{self.provider_name} returned an invalid JSON response."
            ) from e

        try:

            generated_text = (
                response_data["choices"][0]["message"]["content"]
            )

        except (KeyError, IndexError, TypeError) as e:

            raise RuntimeError(
                f"{self.provider_name} returned an unexpected response format."
            ) from e

        if not isinstance(generated_text, str) or not generated_text.strip():

            raise RuntimeError(
                f"{self.provider_name} returned an empty response."
            )

        return {
            "provider": self.provider_name,
            "model": self.model,
            "response": generated_text
        }
