from app.services.schema_context_service import build_schema_context


def build_sql_prompt(user_question: str) -> str:

    schema_context = build_schema_context()

    prompt = f"""
You are an expert MySQL database assistant.

Your task is to convert the user's natural language question
into a valid MySQL SELECT query.

DATABASE SCHEMA:

{schema_context}

RULES:
1. Generate SQL queries using only the tables and columns in the provided schema.
2. Generate SELECT statements only.
3. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE statements.
4. Do not invent table names or column names.
5. Use JOINs when data from multiple related tables is needed.
6. When the user asks to show, list, or retrieve records of an entity, select all relevant basic columns available for that entity, not just its name.
7. For customer queries, include customer_id, customer_name, email, phone, and city whenever these columns exist in the schema.
8. Select only columns relevant to the user's question and avoid unnecessary columns.
9. Use clear column aliases when needed.
10. Return only the SQL query.
11. Do not include explanations or Markdown code blocks.

USER QUESTION:
{user_question}

SQL QUERY:
"""

    return prompt