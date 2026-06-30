"""Refresh dashboard/demo_data.json from PostgreSQL (run after ETL)."""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from etl.db import connect

OUTPUT = Path(__file__).resolve().parent / "demo_data.json"


def export_snapshot() -> dict:
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM fact_routes")
    routes = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dim_airport")
    airports = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dim_airline")
    airlines = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dim_equipment")
    equipment = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM fact_routes WHERE codeshare = true")
    codeshare = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM fact_routes WHERE stops = 0")
    direct = cur.fetchone()[0]

    cur.execute(
        """
        WITH airport_traffic AS (
            SELECT src_airport_id AS airport_id, COUNT(*) AS cnt FROM fact_routes GROUP BY 1
            UNION ALL
            SELECT dst_airport_id, COUNT(*) FROM fact_routes GROUP BY 1
        )
        SELECT a.name, a.country, a.iata_code, SUM(t.cnt)::int
        FROM airport_traffic t
        JOIN dim_airport a ON a.airport_id = t.airport_id
        GROUP BY a.name, a.country, a.iata_code
        ORDER BY 4 DESC LIMIT 10
        """
    )
    top_airports = [
        {"name": r[0], "country": r[1], "iata": r[2], "routes": r[3]} for r in cur.fetchall()
    ]

    cur.execute(
        """
        SELECT al.country, COUNT(r.route_id)::int
        FROM fact_routes r JOIN dim_airline al ON al.airline_id = r.airline_id
        WHERE al.country IS NOT NULL
        GROUP BY al.country ORDER BY 2 DESC LIMIT 15
        """
    )
    routes_by_country = [{"country": r[0], "routes": r[1]} for r in cur.fetchall()]

    cur.execute(
        """
        SELECT e.iata_code, e.aircraft_name, COUNT(r.route_id)::int
        FROM fact_routes r JOIN dim_equipment e ON e.equipment_id = r.equipment_id
        GROUP BY e.iata_code, e.aircraft_name ORDER BY 3 DESC LIMIT 10
        """
    )
    top_aircraft = [{"code": r[0], "name": r[1], "routes": r[2]} for r in cur.fetchall()]
    conn.close()

    return {
        "generated_at": date.today().isoformat(),
        "kpis": {
            "routes": routes,
            "airports": airports,
            "airlines": airlines,
            "equipment": equipment,
            "codeshare_routes": codeshare,
            "direct_routes": direct,
        },
        "top_airports": top_airports,
        "routes_by_country": routes_by_country,
        "top_aircraft": top_aircraft,
    }


def main() -> int:
    snapshot = export_snapshot()
    OUTPUT.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
