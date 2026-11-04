from sqlalchemy import text

from app.core.database import engine
from app.services.sql_validation_service import validate_sql_query


class SQLExecutionService:

    def execute_query(self, query: str) -> dict:

        # Step 1: Validate SQL query
        validation_result = validate_sql_query(query)

        if not validation_result["valid"]:
            return {
                "success": False,
                "message": validation_result["message"],
                "data": []
            }

        # Step 2: Get validated SQL
        validated_sql = validation_result["sql"]

        try:
            # Step 3: Execute SQL
            with engine.connect() as connection:

                result = connection.execute(
                    text(validated_sql)
                )

                rows = result.mappings().all()

                data = [
                    dict(row)
                    for row in rows
                ]

                return {
                    "success": True,
                    "message": "Query executed successfully.",
                    "row_count": len(data),
                    "data": data
                }

        except Exception:
            return {
                "success": False,
                "message": "Database query execution failed.",
                "data": []
            }