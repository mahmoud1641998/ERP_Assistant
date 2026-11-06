
import sqlglot
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify

from app.core.config import settings
from app.services.schema_service import get_database_schema


BLOCKED_FUNCTIONS = {
    "SLEEP",
    "BENCHMARK",
    "LOAD_FILE"
}


def validate_sql_query(query: str) -> dict:

    try:
        parsed_queries = sqlglot.parse(
            query,
            read="mysql"
        )

        if len(parsed_queries) != 1:
            return {
                "valid": False,
                "message": "Only one SQL statement is allowed."
            }

        parsed_query = parsed_queries[0]

        if parsed_query is None:
            return {
                "valid": False,
                "message": "Empty SQL query."
            }

        if not isinstance(parsed_query, exp.Query):
            return {
                "valid": False,
                "message": "Only SELECT queries are allowed."
            }

        if parsed_query.find(exp.Into):
            return {
                "valid": False,
                "message": "SELECT INTO is not allowed."
            }

        if parsed_query.args.get("locks"):
            return {
                "valid": False,
                "message": "Locking queries are not allowed."
            }

        # Block dangerous SQL functions
        blocked_functions = {
            function.this.upper()
            for function in parsed_query.find_all(exp.Anonymous)
            if isinstance(function.this, str)
            and function.this.upper() in BLOCKED_FUNCTIONS
        }

        if blocked_functions:
            return {
                "valid": False,
                "message": "Dangerous SQL functions are not allowed: "
                + ", ".join(sorted(blocked_functions))
            }

        # Validate database and catalog references
        for table in parsed_query.find_all(exp.Table):

            if table.catalog:
                return {
                    "valid": False,
                    "message": "Catalog-qualified table references are not allowed."
                }

            if table.db and table.db.lower() != settings.ERP_DB_NAME.lower():
                return {
                    "valid": False,
                    "message": "Access to databases other than the ERP database is not allowed."
                }

        # Get database schema
        database_schema = get_database_schema()

        # Build allowed tables
        allowed_tables = {
            table.lower()
            for table in database_schema.keys()
        }

        # Extract used tables
        cte_names = {
            cte.alias_or_name.lower()
            for cte in parsed_query.find_all(exp.CTE)
        }

        used_tables = {
            table.name.lower()
            for table in parsed_query.find_all(exp.Table)
        }

        used_tables -= cte_names

        # Validate tables
        invalid_tables = used_tables - allowed_tables

        if invalid_tables:
            return {
                "valid": False,
                "message": "Unknown tables found: "
                + ", ".join(sorted(invalid_tables))
            }

        # Build schema mapping for SQLGlot
        sqlglot_schema = {
            table_name: {
                column["name"]: str(column["type"])
                for column in table_info["columns"]
            }
            for table_name, table_info in database_schema.items()
        }

        # Validate and qualify columns
        qualified_query = qualify(
            parsed_query.copy(),
            dialect="mysql",
            schema=sqlglot_schema,
            validate_qualify_columns=True,
            quote_identifiers=False
        )

        # Enforce maximum result limit
        MAX_ROWS = 100

        limit_expression = qualified_query.args.get("limit")

        if limit_expression is None:
            qualified_query = qualified_query.limit(MAX_ROWS)

        else:
            limit_value = limit_expression.expression

            if isinstance(limit_value, exp.Literal) and limit_value.is_int:
                requested_limit = int(limit_value.this)

                if requested_limit > MAX_ROWS:
                    qualified_query = qualified_query.limit(MAX_ROWS)

            else:
                return {
                    "valid": False,
                    "message": "Only numeric LIMIT values are allowed."
                }

        return {
            "valid": True,
            "message": "SQL query is valid.",
            "sql": qualified_query.sql(dialect="mysql")
        }

    except (sqlglot.errors.ParseError, sqlglot.errors.OptimizeError) as e:
        return {
            "valid": False,
            "message": f"SQL validation failed: {str(e)}"
        }
