"""Refresh dashboard/demo_data.json from PostgreSQL (run after ETL)."""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from etl.db import connect

PROJECT_ROOT = Path(__file__).resolve().parent.parent
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
    cur.execute("SELECT COUNT(*) FROM dim_airline WHERE active = true")
    active_airlines = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dim_airline WHERE active = false")
    inactive_airlines = cur.fetchone()[0]

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
        SELECT al.name, al.country, al.iata_code, COUNT(r.route_id)::int
        FROM fact_routes r
        JOIN dim_airline al ON al.airline_id = r.airline_id
        GROUP BY al.name, al.country, al.iata_code
        ORDER BY 4 DESC LIMIT 10
        """
    )
    top_airlines = [
        {"name": r[0], "country": r[1], "iata": r[2] or "—", "routes": r[3]}
        for r in cur.fetchall()
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

    cur.execute(
        """
        SELECT
            CASE WHEN sa.country = da.country THEN 'Domestic' ELSE 'International' END,
            COUNT(*)::int
        FROM fact_routes r
        JOIN dim_airport sa ON sa.airport_id = r.src_airport_id
        JOIN dim_airport da ON da.airport_id = r.dst_airport_id
        WHERE sa.country IS NOT NULL AND da.country IS NOT NULL
        GROUP BY 1
        """
    )
    route_scope = {r[0]: r[1] for r in cur.fetchall()}

    cur.execute(
        """
        SELECT sa.country, da.country, COUNT(*)::int
        FROM fact_routes r
        JOIN dim_airport sa ON sa.airport_id = r.src_airport_id
        JOIN dim_airport da ON da.airport_id = r.dst_airport_id
        WHERE sa.country IS NOT NULL AND da.country IS NOT NULL
          AND sa.country <> da.country
        GROUP BY sa.country, da.country
        ORDER BY 3 DESC LIMIT 10
        """
    )
    top_country_pairs = [
        {"from": r[0], "to": r[1], "routes": r[2]} for r in cur.fetchall()
    ]

    cur.execute(
        """
        SELECT sa.iata_code, da.iata_code, sa.city, da.city, COUNT(*)::int
        FROM fact_routes r
        JOIN dim_airport sa ON sa.airport_id = r.src_airport_id
        JOIN dim_airport da ON da.airport_id = r.dst_airport_id
        WHERE sa.iata_code IS NOT NULL AND da.iata_code IS NOT NULL
        GROUP BY sa.iata_code, da.iata_code, sa.city, da.city
        ORDER BY 5 DESC LIMIT 10
        """
    )
    top_route_pairs = [
        {
            "from_iata": r[0],
            "to_iata": r[1],
            "from_city": r[2],
            "to_city": r[3],
            "routes": r[4],
        }
        for r in cur.fetchall()
    ]

    conn.close()

    own_operated = routes - codeshare
    return {
        "generated_at": date.today().isoformat(),
        "kpis": {
            "routes": routes,
            "airports": airports,
            "airlines": airlines,
            "equipment": equipment,
            "codeshare_routes": codeshare,
            "own_operated_routes": own_operated,
            "direct_routes": direct,
            "active_airlines": active_airlines,
            "inactive_airlines": inactive_airlines,
        },
        "route_scope": route_scope,
        "codeshare_split": {
            "Codeshare": codeshare,
            "Own operated": own_operated,
        },
        "top_airports": top_airports,
        "top_airlines": top_airlines,
        "routes_by_country": routes_by_country,
        "top_aircraft": top_aircraft,
        "top_country_pairs": top_country_pairs,
        "top_route_pairs": top_route_pairs,
    }


def main() -> int:
    snapshot = export_snapshot()
    OUTPUT.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    pages_data = PROJECT_ROOT.parent / "docs" / "data.json"
    if pages_data.parent.exists():
        pages_data.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
        print(f"Wrote {pages_data}")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
