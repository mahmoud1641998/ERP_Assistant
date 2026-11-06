
from app.services.conversation_prompt_service import (
    build_conversation_sql_prompt
)

from app.llm.factory import LLMFactory

from app.services.sql_validation_service import validate_sql_query


class ConversationSQLGenerationService:

    def __init__(self):
        self.llm_provider = LLMFactory.get_provider()

    def generate_sql(
        self,
        user_question: str,
        conversation_history: list[dict]
    ):

        prompt = build_conversation_sql_prompt(
            user_question=user_question,
            conversation_history=conversation_history
        )

        response = self.llm_provider.generate_response(
            prompt=prompt
        )

        generated_sql = response["response"]

        validation_result = validate_sql_query(generated_sql)

        if not validation_result["valid"]:

            return {
                "success": False,
                "question": user_question,
                "sql": generated_sql,
                "model": response["model"],
                "message": validation_result["message"]
            }

        return {
            "success": True,
            "question": user_question,
            "sql": validation_result["sql"],
            "model": response["model"],
            "message": "SQL query generated and validated successfully."
        }
