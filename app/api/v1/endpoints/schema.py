from fastapi import APIRouter, HTTPException

from app.services.schema_service import get_database_schema


router = APIRouter()


@router.get("/schema")
def inspect_database_schema():
    try:
        schema = get_database_schema()

        return {
            "status": "success",
            "tables_count": len(schema),
            "schema": schema
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )