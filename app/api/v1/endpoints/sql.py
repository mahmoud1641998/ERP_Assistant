import logging

from fastapi import APIRouter, HTTPException

from app.schemas.sql import (
    SQLGenerationRequest,
    SQLGenerationResponse
)

from app.services.sql_generation_service import SQLGenerationService
from app.services.sql_validation_service import validate_sql_query


logger = logging.getLogger(__name__)

router = APIRouter()

sql_generation_service = SQLGenerationService()


@router.post(
    "/generate",
    response_model=SQLGenerationResponse
)
def generate_sql(request: SQLGenerationRequest):

    try:
        # Step 1: Generate SQL using LLM Provider
        generation_result = sql_generation_service.generate_sql(
            request.question
        )

        generated_sql = generation_result["sql"]

        # Step 2: Validate generated SQL
        validation_result = validate_sql_query(generated_sql)

        if not validation_result["valid"]:
            raise HTTPException(
                status_code=422,
                detail=validation_result["message"]
            )

        # Step 3: Return validated SQL without execution
        return SQLGenerationResponse(
            success=True,
            question=request.question,
            sql=validation_result["sql"],
            model=generation_result["model"],
            message="SQL generated and validated successfully."
        )

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error in SQL generation endpoint")

        raise HTTPException(
            status_code=500,
            detail="SQL generation failed."
        )