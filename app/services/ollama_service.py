import ollama


class OllamaService:

    def __init__(self):
        self.client = ollama.Client(
            host="http://localhost:11434"
        )

    def check_connection(self):
        try:
            response = self.client.list()

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
            raise Exception(f"Failed to retrieve models: {str(e)}")

    def generate_response(self, prompt: str, model: str):

        try:
            response = self.client.generate(
                model=model,
                prompt=prompt,
                stream=False,
                options={
                        "num_predict": 200,
                        "temperature": 0.1,
                        }
            )

            return {
            "model": model,
            "response": response.response
            }

        except Exception as e:
            raise Exception(f"Generation failed: {str(e)}")