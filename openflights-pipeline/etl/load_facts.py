from pathlib import Path

from psycopg2.extensions import connection
from psycopg2.extras import execute_batch

from etl.config import DATA_DIR
from etl.parsers import parse_routes


def _equipment_lookup(conn: connection) -> dict[str, int]:
    with conn.cursor() as cur:
        cur.execute("SELECT equipment_id, iata_code FROM dim_equipment")
        return {row[1]: row[0] for row in cur.fetchall()}


def load_routes(conn: connection, data_dir: Path = DATA_DIR) -> dict[str, int]:
    equipment_by_iata = _equipment_lookup(conn)
    to_insert: list[dict] = []
    skipped = 0

    for route in parse_routes(data_dir / "routes.dat"):
        equipment_id = None
        if route["equipment_iata"]:
            equipment_id = equipment_by_iata.get(route["equipment_iata"])

        if (
            route["airline_id"] is None
            or route["src_airport_id"] is None
            or route["dst_airport_id"] is None
        ):
            skipped += 1
            continue

        to_insert.append(
            {
                "airline_id": route["airline_id"],
                "src_airport_id": route["src_airport_id"],
                "dst_airport_id": route["dst_airport_id"],
                "equipment_id": equipment_id,
                "codeshare": route["codeshare"],
                "stops": route["stops"],
            }
        )

    with conn.cursor() as cur:
        execute_batch(
            cur,
            """
            INSERT INTO fact_routes (
                airline_id, src_airport_id, dst_airport_id,
                equipment_id, codeshare, stops
            )
            SELECT %(airline_id)s, %(src_airport_id)s, %(dst_airport_id)s,
                   %(equipment_id)s, %(codeshare)s, %(stops)s
            WHERE EXISTS (SELECT 1 FROM dim_airline WHERE airline_id = %(airline_id)s)
              AND EXISTS (SELECT 1 FROM dim_airport WHERE airport_id = %(src_airport_id)s)
              AND EXISTS (SELECT 1 FROM dim_airport WHERE airport_id = %(dst_airport_id)s)
            """,
            to_insert,
            page_size=1000,
        )

    conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM fact_routes")
        loaded = cur.fetchone()[0]

    return {
        "parsed": len(to_insert),
        "loaded": loaded,
        "skipped_invalid_ids": skipped,
        "skipped_missing_fk": len(to_insert) - loaded,
    }
