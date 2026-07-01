"""Run the Phase 2 ETL: load OpenFlights .dat files into PostgreSQL."""

import argparse
import sys

from etl.db import connect, init_schema
from etl.load_dimensions import load_all_dimensions
from etl.load_facts import load_routes


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenFlights ETL pipeline")
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create tables from sql/schema.sql before loading",
    )
    parser.add_argument(
        "--dimensions-only",
        action="store_true",
        help="Load dimension tables only (skip fact_routes)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run Soda Core data quality checks after loading",
    )
    args = parser.parse_args()

    try:
        conn = connect()
    except Exception as exc:
        print(f"Database connection failed: {exc}")
        print("Check .env and that PostgreSQL is running (see DOCUMENTATION.md).")
        return 1

    try:
        if args.init:
            print("Creating schema...")
            init_schema(conn)
            print("Schema ready.")

        print("Loading dimensions...")
        dim_counts = load_all_dimensions(conn)
        for name, count in dim_counts.items():
            print(f"  {name}: {count} rows parsed")

        if not args.dimensions_only:
            print("Loading fact_routes...")
            fact_stats = load_routes(conn)
            print(f"  parsed: {fact_stats['parsed']}")
            print(f"  loaded: {fact_stats['loaded']}")
            print(f"  skipped (null ids): {fact_stats['skipped_invalid_ids']}")
            print(f"  skipped (missing FK): {fact_stats['skipped_missing_fk']}")

        print("ETL complete.")
    finally:
        conn.close()

    if args.validate and not args.dimensions_only:
        print("Running data quality checks...")
        from quality.run_checks import run_checks

        code = run_checks()
        if code != 0:
            print("Data quality checks failed.")
            return code
        print("Data quality checks passed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
