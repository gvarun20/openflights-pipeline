"""Run Soda Core data quality checks against the warehouse."""

import os
import subprocess
import sys
from pathlib import Path

QUALITY_DIR = Path(__file__).resolve().parent


def _ensure_db_env() -> None:
    from etl.config import db_config

    cfg = db_config()
    os.environ.setdefault("DB_HOST", cfg["host"])
    os.environ.setdefault("DB_PORT", str(cfg["port"]))
    os.environ.setdefault("DB_NAME", cfg["dbname"])
    os.environ.setdefault("DB_USER", cfg["user"])
    os.environ.setdefault("DB_PASSWORD", cfg["password"])


def run_checks(verbose: bool = False) -> int:
    _ensure_db_env()
    cmd = [
        sys.executable,
        "-m",
        "soda",
        "scan",
        "-d",
        "openflights_dw",
        "-c",
        str(QUALITY_DIR / "configuration.yml"),
        str(QUALITY_DIR / "checks.yml"),
    ]
    if verbose:
        cmd.append("-V")
    result = subprocess.run(cmd, cwd=QUALITY_DIR.parent)
    return result.returncode


def main() -> int:
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    return run_checks(verbose=verbose)


if __name__ == "__main__":
    sys.exit(main())
