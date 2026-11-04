from sqlalchemy.orm import Session

from app.services.conversation_service import ConversationService

from app.services.conversation_sql_generation_service import (
    ConversationSQLGenerationService
)

from app.services.sql_execution_service import SQLExecutionService

from app.services.answer_generation_service import AnswerGenerationService


class ConversationAssistantService:

    def __init__(self):

        self.conversation_service = ConversationService()

        self.sql_generation_service = (
            ConversationSQLGenerationService()
        )

        self.sql_execution_service = SQLExecutionService()

        self.answer_generation_service = AnswerGenerationService()

    def get_or_create_conversation(
        self,
        db: Session,
        conversation_id: int | None = None
    ):

        if conversation_id is None:

            return self.conversation_service.create_conversation(
                db=db
            )

        return self.conversation_service.get_conversation(
            db=db,
            conversation_id=conversation_id
        )

    def get_conversation_history(
        self,
        db: Session,
        conversation_id: int
    ):

        messages = self.conversation_service.get_messages(
            db=db,
            conversation_id=conversation_id
        )

        return [
            {
                "role": message.role,
                "content": message.content
            }
            for message in messages
        ]

    def save_user_message(
        self,
        db: Session,
        conversation_id: int,
        content: str
    ):

        return self.conversation_service.add_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=content
        )

    def save_assistant_message(
        self,
        db: Session,
        conversation_id: int,
        content: str
    ):

        return self.conversation_service.add_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=content
        )

    def ask(
        self,
        db: Session,
        user_question: str,
        conversation_id: int | None = None
    ):

        # Step 1: Get or create conversation
        conversation = self.get_or_create_conversation(
            db=db,
            conversation_id=conversation_id
        )

        if conversation is None:

            return {
                "success": False,
                "conversation_id": conversation_id,
                "question": user_question,
                "sql": None,
                "model": None,
                "message": "Conversation not found."
            }

        # Step 2: Retrieve previous conversation history
        conversation_history = self.get_conversation_history(
            db=db,
            conversation_id=conversation.id
        )

        # Step 3: Save current user question
        self.save_user_message(
            db=db,
            conversation_id=conversation.id,
            content=user_question
        )

        # Step 4: Generate and validate SQL
        generation_result = self.sql_generation_service.generate_sql(
            user_question=user_question,
            conversation_history=conversation_history
        )

        if not generation_result["success"]:

            self.save_assistant_message(
                db=db,
                conversation_id=conversation.id,
                content=generation_result["message"]
            )

            return {
                **generation_result,
                "conversation_id": conversation.id
            }

        generated_sql = generation_result["sql"]

        # Step 5: Execute SQL
        execution_result = self.sql_execution_service.execute_query(
            query=generated_sql
        )

        if not execution_result["success"]:

            self.save_assistant_message(
                db=db,
                conversation_id=conversation.id,
                content=execution_result["message"]
            )

            return {
                "success": False,
                "conversation_id": conversation.id,
                "question": user_question,
                "sql": generated_sql,
                "model": generation_result["model"],
                "message": execution_result["message"],
                "row_count": 0,
                "data": [],
                "answer": None
            }

        # Step 6: Generate natural language answer
        try:

            answer_result = self.answer_generation_service.generate_answer(
                user_question=user_question,
                sql_query=generated_sql,
                query_results={
                    "row_count": execution_result["row_count"],
                    "data": execution_result["data"]
                }
            )

            answer = answer_result["answer"]

        except Exception:

            error_message = (
                "Query executed successfully, "
                "but answer generation failed."
            )

            self.save_assistant_message(
                db=db,
                conversation_id=conversation.id,
                content=error_message
            )

            return {
                "success": False,
                "conversation_id": conversation.id,
                "question": user_question,
                "sql": generated_sql,
                "model": generation_result["model"],
                "message": error_message,
                "row_count": execution_result["row_count"],
                "data": execution_result["data"],
                "answer": None
            }

        # Step 7: Save assistant answer
        self.save_assistant_message(
            db=db,
            conversation_id=conversation.id,
            content=answer
        )

        # Step 8: Return final response
        return {
            "success": True,
            "conversation_id": conversation.id,
            "question": user_question,
            "sql": generated_sql,
            "model": generation_result["model"],
            "message": execution_result["message"],
            "row_count": execution_result["row_count"],
            "data": execution_result["data"],
            "answer": answer
        }