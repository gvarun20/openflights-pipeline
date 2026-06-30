from pathlib import Path

from psycopg2.extensions import connection
from psycopg2.extras import execute_batch

from etl.config import DATA_DIR
from etl.db import reset_serial
from etl.parsers import parse_airlines, parse_airports, parse_equipment


def load_airports(conn: connection, data_dir: Path = DATA_DIR) -> int:
    rows = list(parse_airports(data_dir / "airports.dat"))
    with conn.cursor() as cur:
        execute_batch(
            cur,
            """
            INSERT INTO dim_airport (
                airport_id, name, city, country, iata_code, icao_code,
                latitude, longitude, altitude_ft, timezone_utc
            )
            OVERRIDING SYSTEM VALUE
            VALUES (%(airport_id)s, %(name)s, %(city)s, %(country)s,
                    %(iata_code)s, %(icao_code)s, %(latitude)s, %(longitude)s,
                    %(altitude_ft)s, %(timezone_utc)s)
            ON CONFLICT (airport_id) DO NOTHING
            """,
            rows,
            page_size=500,
        )
    conn.commit()
    reset_serial(conn, "dim_airport", "airport_id")
    return len(rows)


def load_airlines(conn: connection, data_dir: Path = DATA_DIR) -> int:
    rows = list(parse_airlines(data_dir / "airlines.dat"))
    with conn.cursor() as cur:
        execute_batch(
            cur,
            """
            INSERT INTO dim_airline (
                airline_id, name, iata_code, icao_code, country, active,
                valid_from, valid_to, is_current
            )
            OVERRIDING SYSTEM VALUE
            VALUES (
                %(airline_id)s, %(name)s, %(iata_code)s, %(icao_code)s,
                %(country)s, %(active)s, CURRENT_DATE, NULL, TRUE
            )
            ON CONFLICT (airline_id) DO NOTHING
            """,
            rows,
            page_size=500,
        )
    conn.commit()
    reset_serial(conn, "dim_airline", "airline_id")
    return len(rows)


def load_equipment(conn: connection, data_dir: Path = DATA_DIR) -> int:
    rows = list(parse_equipment(data_dir / "planes.dat"))
    with conn.cursor() as cur:
        execute_batch(
            cur,
            """
            INSERT INTO dim_equipment (iata_code, aircraft_name, category)
            VALUES (%(iata_code)s, %(aircraft_name)s, %(category)s)
            ON CONFLICT (iata_code) DO NOTHING
            """,
            rows,
            page_size=200,
        )
    conn.commit()
    return len(rows)


def load_all_dimensions(conn: connection, data_dir: Path = DATA_DIR) -> dict[str, int]:
    return {
        "airports": load_airports(conn, data_dir),
        "airlines": load_airlines(conn, data_dir),
        "equipment": load_equipment(conn, data_dir),
    }
