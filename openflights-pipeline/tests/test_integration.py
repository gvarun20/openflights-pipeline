"""Integration tests against a loaded PostgreSQL warehouse."""

import pytest

from etl.db import connect

pytestmark = pytest.mark.integration


@pytest.fixture
def db():
    try:
        conn = connect()
    except Exception as exc:
        pytest.skip(f"PostgreSQL not available: {exc}")
    yield conn
    conn.close()


def test_fact_routes_count(db):
    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM fact_routes")
        count = cur.fetchone()[0]
    assert 65000 <= count <= 67000


def test_no_null_route_foreign_keys(db):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*) FROM fact_routes
            WHERE airline_id IS NULL
               OR src_airport_id IS NULL
               OR dst_airport_id IS NULL
            """
        )
        nulls = cur.fetchone()[0]
    assert nulls == 0


def test_top_hub_is_atlanta(db):
    with db.cursor() as cur:
        cur.execute(
            """
            WITH traffic AS (
                SELECT src_airport_id AS airport_id, COUNT(*) AS cnt
                FROM fact_routes GROUP BY 1
                UNION ALL
                SELECT dst_airport_id, COUNT(*) FROM fact_routes GROUP BY 1
            )
            SELECT a.iata_code
            FROM traffic t
            JOIN dim_airport a ON a.airport_id = t.airport_id
            GROUP BY a.iata_code
            ORDER BY SUM(t.cnt) DESC
            LIMIT 1
            """
        )
        top_iata = cur.fetchone()[0]
    assert top_iata == "ATL"


def test_top_airline_is_ryanair(db):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT al.name
            FROM fact_routes r
            JOIN dim_airline al ON al.airline_id = r.airline_id
            GROUP BY al.name
            ORDER BY COUNT(*) DESC
            LIMIT 1
            """
        )
        top_name = cur.fetchone()[0]
    assert top_name == "Ryanair"


def test_soda_quality_checks_pass():
    from quality.run_checks import run_checks

    assert run_checks() == 0
