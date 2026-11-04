from app.services.sql_generation_service import SQLGenerationService
from app.services.sql_execution_service import SQLExecutionService
from app.services.answer_generation_service import AnswerGenerationService


class SQLAssistantService:

    def __init__(self):
        self.sql_generation_service = SQLGenerationService()
        self.sql_execution_service = SQLExecutionService()
        self.answer_generation_service = AnswerGenerationService()

    def ask(self, user_question: str) -> dict:

        # Step 1: Generate SQL
        generation_result = self.sql_generation_service.generate_sql(
            user_question
        )

        generated_sql = generation_result["sql"]

        # Step 2: Execute SQL (includes validation)
        execution_result = self.sql_execution_service.execute_query(
            generated_sql
        )

        # Step 3: Stop if execution fails
        if not execution_result["success"]:
            return {
                "success": False,
                "question": user_question,
                "generated_sql": generated_sql,
                "message": execution_result["message"],
                "row_count": 0,
                "data": [],
                "answer": None,
                "model": generation_result["model"]
            }

        # Step 4: Generate natural language answer
        answer_result = self.answer_generation_service.generate_answer(
            user_question=user_question,
            sql_query=generated_sql,
            query_results={
                "row_count": execution_result["row_count"],
                "data": execution_result["data"]
            }
        )

        # Step 5: Return complete response
        return {
            "success": True,
            "question": user_question,
            "generated_sql": generated_sql,
            "message": execution_result["message"],
            "row_count": execution_result["row_count"],
            "data": execution_result["data"],
            "answer": answer_result["answer"],
            "model": generation_result["model"]
        }