from app.services.prompt_service import build_sql_prompt
from app.services.ollama_service import OllamaService


class SQLGenerationService:

    def __init__(self):
        self.ollama_service = OllamaService()

    def generate_sql(self, user_question: str):

        prompt = build_sql_prompt(user_question)

        response = self.ollama_service.generate_response(
            prompt=prompt,
            model="qwen3:4b-instruct-2507-q4_K_M"
        )

        return {
            "question": user_question,
            "sql": response["response"],
            "model": response["model"]
        }