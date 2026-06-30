# Architecture & Design Decisions

## Data flow

```
airports.dat ──┐
airlines.dat ──┼──► parsers.py ──► load_dimensions.py ──► dim_*
planes.dat   ──┘                              │
                                              ▼
routes.dat ──────────────────────► load_facts.py ──► fact_routes
                                              │
                                              ▼
                                    sql/queries.sql (analytics)
                                              │
                                              ▼
                                    dashboard/app.py (Streamlit)
```

## Star schema

| Table | Type | Purpose |
|-------|------|---------|
| `fact_routes` | Fact | One row per airline route (origin → destination) |
| `dim_airport` | Dimension | Airport attributes; used twice (source + destination) |
| `dim_airline` | Dimension | Airline attributes; SCD Type 2 columns for history |
| `dim_equipment` | Dimension | Aircraft type (IATA code) |
| `dim_date` | Dimension | Calendar attributes (reserved for future schedule data) |

## Key design decisions

### Star vs snowflake
Chose **star schema** for simpler JOINs. Airport country is stored on `dim_airport` rather than normalising to a separate country table.

### Role-playing dimension
`fact_routes` has two FKs to `dim_airport` (`src_airport_id`, `dst_airport_id`) — same table, two roles.

### SCD Type 2 on airlines
`valid_from`, `valid_to`, `is_current` columns support tracking airline renames/mergers in future loads.

### Data quality in ETL
- Invalid IATA/ICAO codes → NULL
- Routes with missing FK references → skipped (~449 rows)
- Corrupt source rows → cleaned at parse time

## Infrastructure

| Component | Role |
|-----------|------|
| Docker | Reproducible ETL + Postgres environment |
| GitHub Actions | Lint, test, Docker build on every push |
| Streamlit | Live dashboard; demo mode uses committed JSON snapshot |

## Why no AWS?

AWS requires a credit card even for free tier. This project demonstrates the same engineering skills (ETL, warehousing, Docker, CI/CD, analytics) using **free, local-first tools** that recruiters can verify on GitHub without cloud cost.

Cloud deployment can be added later with Streamlit Cloud (free) or Neon PostgreSQL (free tier, email signup).
