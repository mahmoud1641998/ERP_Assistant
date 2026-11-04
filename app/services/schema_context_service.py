from app.services.schema_service import get_database_schema


def build_schema_context() -> str:
    schema = get_database_schema()

    context_parts = []

    for table_name, table_info in schema.items():

        context_parts.append(f"Table: {table_name}")

        context_parts.append("Columns:")

        for column in table_info["columns"]:
            column_description = (
                f"- {column['name']} "
                f"({column['type']})"
            )

            if not column["nullable"]:
                column_description += " NOT NULL"

            context_parts.append(column_description)

        primary_keys = table_info["primary_key"]

        if primary_keys:
            context_parts.append(
                f"Primary Key: {', '.join(primary_keys)}"
            )

        for foreign_key in table_info["foreign_keys"]:
            relationship = (
                f"Foreign Key: "
                f"{', '.join(foreign_key['columns'])} "
                f"references "
                f"{foreign_key['referenced_table']}."
                f"{', '.join(foreign_key['referenced_columns'])}"
            )

            context_parts.append(relationship)

        context_parts.append("")

    return "\n".join(context_parts)