
from app.services.prompt_service import build_sql_prompt
from app.llm.factory import LLMFactory


class SQLGenerationService:

    def __init__(self):
        self.llm_provider = LLMFactory.get_provider()

    def generate_sql(self, user_question: str):

        prompt = build_sql_prompt(user_question)

        response = self.llm_provider.generate_response(
            prompt=prompt
        )

        return {
            "question": user_question,
            "sql": response["response"],
            "model": response["model"]
        }
