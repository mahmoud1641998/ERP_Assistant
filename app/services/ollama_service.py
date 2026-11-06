import ollama

from app.core.config import settings


class OllamaService:

    def __init__(self):

        self.client = ollama.Client(
            host=settings.OLLAMA_BASE_URL,
            timeout=settings.LLM_TIMEOUT
        )

    def check_connection(self):

        try:
            self.client.list()

            return {
                "status": "connected",
                "message": "Ollama is running"
            }

        except Exception as e:

            return {
                "status": "disconnected",
                "message": str(e)
            }

    def get_models(self):

        try:
            response = self.client.list()

            models = []

            for model in response.models:

                models.append({
                    "name": model.model,
                    "size": model.size
                })

            return models

        except Exception as e:

            raise Exception(
                f"Failed to retrieve models: {str(e)}"
            )