
from sqlalchemy import inspect

from app.core.database import erp_engine


def get_database_schema():
    inspector = inspect(erp_engine)

    schema = {}

    for table_name in inspector.get_table_names():

        columns = inspector.get_columns(table_name)
        primary_keys = inspector.get_pk_constraint(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)

        schema[table_name] = {
            "columns": [
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                    "default": column["default"]
                }
                for column in columns
            ],

            "primary_key": primary_keys.get("constrained_columns", []),

            "foreign_keys": [
                {
                    "columns": fk["constrained_columns"],
                    "referenced_table": fk["referred_table"],
                    "referenced_columns": fk["referred_columns"]
                }
                for fk in foreign_keys
            ]
        }

    return schema
