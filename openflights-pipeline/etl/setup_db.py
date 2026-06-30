"""Create openflights_dw database if it does not exist."""

import sys

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from etl.config import db_config


def main() -> int:
    cfg = db_config()
    db_name = cfg["dbname"]
    admin_cfg = {**cfg, "dbname": "postgres"}

    try:
        conn = psycopg2.connect(**admin_cfg)
    except psycopg2.Error as exc:
        print(f"Connection failed: {exc}")
        print("Check DB_HOST, DB_USER, and DB_PASSWORD in .env or container env.")
        return 1

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if cur.fetchone():
            print(f"Database '{db_name}' already exists.")
        else:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Created database '{db_name}'.")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
