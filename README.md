# Open Flights Data Pipeline

[![CI Pipeline](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml)

Data warehouse ETL pipeline with star schema (PostgreSQL, Python, Docker, CI/CD).

## Project structure

| Path | What it is |
|------|------------|
| `sql/` | Database schema and analytics queries (Phase 1) |
| `openflights-pipeline/data/` | Raw OpenFlights `.dat` files |
| `openflights-pipeline/etl/` | Python ETL code (Phase 2) |
| `openflights-pipeline/tests/` | Automated tests (Phase 3) |
| `openflights-pipeline/Dockerfile` | Container image for the ETL |
| `openflights-pipeline/docker-compose.yml` | Postgres + ETL together |

## Docs

Full design notes and run instructions: [openflights-pipeline/docs/README.md](openflights-pipeline/docs/README.md)

## Quick start (Docker)

```bash
cd openflights-pipeline
docker compose up --build
```

## Quick start (local Python)

```bash
cd openflights-pipeline
py -m pip install -r requirements.txt
# Edit .env with your PostgreSQL password
py scripts/setup_db.py
py -m etl.run_etl --init
```

## Tests

```bash
cd openflights-pipeline
py -m pip install -r requirements-dev.txt
pytest tests/ -v
```
