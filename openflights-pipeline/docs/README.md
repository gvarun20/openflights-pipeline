# Open Flights Data Pipeline

[![CI Pipeline](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml)

## Project Overview
A data warehouse for Open Flights data with a star schema design.

## Schema Design

### Star Schema Architecture
The design uses a star schema with:
- **Fact table**: `fact_routes` (routes, airlines, equipment)
- **Dimensions**: airports, airlines, equipment, date

### Key Design Decisions

#### 1. Star vs Snowflake
**Decision**: Star schema (no further normalization)
**Why**: Query simplicity. Airports don't normalize further (country is rare to aggregate separately). Storage cost is negligible.

#### 2. Two FKs to dim_airport (Role-Playing Dimension)
**Decision**: `src_airport_id` and `dst_airport_id` both reference `dim_airport`
**Why**: A route has an origin and destination — both are airports. Rather than duplicate the table, we use role-playing: same dimension, two roles.

#### 3. SCD Type 2 on dim_airline
**Decision**: Columns `valid_from`, `valid_to`, `is_current`
**Why**: Airlines merge, rename, go bankrupt. We preserve history. Queries filter `WHERE is_current = TRUE` for current state.

#### 4. dim_date as a Separate Table
**Decision**: Include date dimension even though routes don't have timestamps yet
**Why**: Future-proofs the schema. When flight schedules are added, date fields are ready. Enables day-of-week, season, holiday analytics.

#### 5. Indexes on Foreign Keys Only
**Decision**: `idx_fact_src`, `idx_fact_dst`, `idx_fact_airl` on fact table FKs
**Why**: JOINs use these columns. We didn't index every column (premature optimization).

## SQL Queries

See `sql/queries.sql` for:
- Top 10 busiest airports (CTEs)
- Airlines ranked by country (window functions)
- Running totals (OVER clauses)
- Bidirectional routes (self-joins)
- Data quality checks (missing sources)
- EXPLAIN ANALYZE results

## Phase 2 — Python ETL (load .dat → PostgreSQL)

### What the ETL does

1. **Extract** — reads `data/*.dat` (OpenFlights CSV format, `\N` = null)
2. **Transform** — maps columns to your star schema; preserves OpenFlights `airport_id` / `airline_id` so `routes.dat` foreign keys resolve
3. **Load** — batch inserts into `dim_airport`, `dim_airline`, `dim_equipment`, then `fact_routes`

Routes that reference missing airlines/airports are skipped (common in OpenFlights). Equipment is matched by IATA code (e.g. `CR2`).

`dim_date` is not populated yet (no dates in route data — reserved for Phase 3+).

### Your setup (one-time)

**1. Python 3.10+** — you have `py` (Python 3.12). Use `py`, not `python`, if `python` is not on PATH.

**2. PostgreSQL** — pick one:

| Option | Steps |
|--------|--------|
| **Docker (recommended)** | Install [Docker Desktop](https://www.docker.com/products/docker-desktop/), then from `openflights-pipeline`: `docker compose up -d` |
| **Local install** | Install [PostgreSQL](https://www.postgresql.org/download/windows/), create database `openflights_dw`, user/password matching `.env` |

**3. Project env**

Edit `.env` and set `DB_PASSWORD` to the password you chose when installing PostgreSQL (default user `postgres`).

```powershell
cd E:\SUMMER_PROJECT\openflights-pipeline
py -m pip install -r requirements.txt
py scripts/setup_db.py
```

### Run the pipeline

```powershell
cd E:\SUMMER_PROJECT\openflights-pipeline
py -m etl.run_etl --init
```

- `--init` — drops existing tables, recreates schema from `sql/schema.sql`, loads all data
- `--dimensions-only` — load dimensions only (useful for debugging)

### Verify

Connect to the DB and run a query from `sql/queries.sql`, e.g. top 10 busiest airports.

Docker:

```powershell
docker exec -it openflights-postgres psql -U openflights -d openflights_dw -c "SELECT COUNT(*) FROM fact_routes;"
```

### ETL layout

```
openflights-pipeline/etl/
  config.py          # paths + DB settings from .env
  db.py              # connect, init schema
  parsers.py         # parse .dat files
  load_dimensions.py # dim_airport, dim_airline, dim_equipment
  load_facts.py      # fact_routes
  run_etl.py         # entry point
```

### Next steps (Phase 4+)

- Populate `dim_date` and add schedule/time analytics
- Dashboards or BI on top of `queries.sql`
- SCD Type 2 updates when airline data changes between loads
- AWS deployment (Lambda / container)

## Phase 3 — Docker & CI/CD

### What Phase 3 adds (in plain English)

Phase 2 made the pipeline work on **your** machine. Phase 3 makes it work on **any** machine — and proves it automatically on every GitHub push.

| Piece | Simple analogy |
|-------|----------------|
| **Dockerfile** | A recipe that packages Python + your code into one box |
| **docker-compose** | Starts the database box and ETL box together, wired to talk |
| **pytest** | Robot checks that your parsers still work after code changes |
| **GitHub Actions** | GitHub runs those robot checks every time you `git push` |

### Docker quick start

```powershell
cd E:\SUMMER_PROJECT\openflights-pipeline
docker compose up --build
```

This starts Postgres, waits until it is healthy, then runs the full ETL (`--init` once).

Verify:

```powershell
docker exec openflights-postgres psql -U openflights -d openflights_dw -c "SELECT COUNT(*) FROM fact_routes;"
```

Stop: `docker compose down` (data persists). Reset data: `docker compose down -v`.

**Note:** Docker uses user `openflights` / password `openflights`. Your local `.env` may still use `postgres` — that is fine; they are separate environments.

### Tests

```powershell
cd E:\SUMMER_PROJECT\openflights-pipeline
py -m pip install -r requirements-dev.txt
py -m pytest tests/ -v
```

### CI/CD

Workflow file: `.github/workflows/ci.yml` (repo root). On push to `main`:

1. Installs Python dependencies
2. Runs pytest
3. Builds the Docker image

Push to GitHub to activate the green badge on README.