from pathlib import Path

import psycopg2
from psycopg2.extensions import connection

from etl.config import db_config, SCHEMA_PATH


def connect() -> connection:
    return psycopg2.connect(**db_config())


def drop_schema(conn: connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            DROP TABLE IF EXISTS fact_routes CASCADE;
            DROP TABLE IF EXISTS dim_date CASCADE;
            DROP TABLE IF EXISTS dim_equipment CASCADE;
            DROP TABLE IF EXISTS dim_airline CASCADE;
            DROP TABLE IF EXISTS dim_airport CASCADE;
            """
        )
    conn.commit()


def init_schema(conn: connection, schema_path: Path = SCHEMA_PATH) -> None:
    drop_schema(conn)
    sql = schema_path.read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def reset_serial(conn: connection, table: str, column: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT setval(
                pg_get_serial_sequence(%s, %s),
                COALESCE((SELECT MAX({column}) FROM {table}), 1)
            )
            """,
            (table, column),
        )
    conn.commit()
