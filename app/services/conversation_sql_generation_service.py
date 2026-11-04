from app.services.conversation_prompt_service import (
    build_conversation_sql_prompt
)

from app.services.ollama_service import OllamaService

from app.services.sql_validation_service import (
    validate_sql_query
)


class ConversationSQLGenerationService:

    def __init__(self):

        self.ollama_service = OllamaService()

    def generate_sql(
        self,
        user_question: str,
        conversation_history: list[dict]
    ):

        # Step 1: Build conversation-aware prompt
        prompt = build_conversation_sql_prompt(
            user_question=user_question,
            conversation_history=conversation_history
        )

        # Step 2: Generate SQL using Ollama
        response = self.ollama_service.generate_response(
            prompt=prompt,
            model="qwen3:4b-instruct-2507-q4_K_M"
        )

        generated_sql = response["response"]

        # Step 3: Validate generated SQL
        validation_result = validate_sql_query(
            generated_sql
        )

        if not validation_result["valid"]:

            return {
                "success": False,
                "question": user_question,
                "sql": generated_sql,
                "model": response["model"],
                "message": validation_result["message"]
            }

        # Step 4: Return validated SQL
        return {
            "success": True,
            "question": user_question,
            "sql": validation_result["sql"],
            "model": response["model"],
            "message": "SQL query generated and validated successfully."
        }