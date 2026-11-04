
from fastapi import APIRouter, HTTPException

from app.schemas.sql import (
    SQLGenerationRequest,
    SQLGenerationResponse
)

from app.services.sql_generation_service import SQLGenerationService
from app.services.sql_validation_service import validate_sql_query


router = APIRouter()

sql_generation_service = SQLGenerationService()


@router.post(
    "/generate",
    response_model=SQLGenerationResponse
)
def generate_sql(request: SQLGenerationRequest):

    try:
        # Step 1: Generate SQL using Ollama
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
        # Preserve HTTP errors raised intentionally
        raise

    except Exception:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail="SQL generation failed."
        )
