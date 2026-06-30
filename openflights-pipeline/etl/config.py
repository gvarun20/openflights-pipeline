import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

_local_schema = PROJECT_ROOT / "sql" / "schema.sql"
_repo_schema = PROJECT_ROOT.parent / "sql" / "schema.sql"
SCHEMA_PATH = _local_schema if _local_schema.exists() else _repo_schema

load_dotenv(PROJECT_ROOT / ".env")


def db_config() -> dict:
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "openflights_dw"),
        "user": os.getenv("DB_USER", "openflights"),
        "password": os.getenv("DB_PASSWORD", "openflights"),
    }
