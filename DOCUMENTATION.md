# Open Flights Data Pipeline — Full Documentation

[![CI Pipeline](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml)
[![Live Dashboard](https://img.shields.io/badge/dashboard-live-3b82f6?style=flat&logo=github)](https://gvarun20.github.io/openflights-pipeline/)

> End-to-end data engineering project: raw OpenFlights aviation data → star-schema PostgreSQL warehouse → Docker → CI/CD → live GitHub Pages dashboard.

| | |
|---|---|
| **Live dashboard** | https://gvarun20.github.io/openflights-pipeline/ |
| **Repository** | https://github.com/gvarun20/openflights-pipeline |
| **CI runs** | https://github.com/gvarun20/openflights-pipeline/actions |
| **Routes loaded** | **66,316** |
| **License** | MIT |

---

## Table of contents

1. [Project summary](#1-project-summary)
2. [Complete tech stack](#2-complete-tech-stack)
3. [Dependencies](#3-dependencies)
4. [Project phases](#4-project-phases)
5. [Data sources](#5-data-sources)
6. [Data model (star schema)](#6-data-model-star-schema)
7. [ETL pipeline](#7-etl-pipeline)
8. [Dashboard](#8-dashboard)
9. [Docker](#9-docker)
10. [CI/CD (GitHub Actions)](#10-cicd-github-actions)
11. [Repository structure](#11-repository-structure)
12. [Setup guide](#12-setup-guide)
13. [Environment variables](#13-environment-variables)
14. [SQL analytics](#14-sql-analytics)
15. [Testing](#15-testing)
16. [Key metrics & insights](#16-key-metrics--insights)
17. [Skills demonstrated](#17-skills-demonstrated)

---

## 1. Project summary

### Problem
OpenFlights publishes raw `.dat` files (~67k flight routes). They are not structured for analytics — no relational model, no data quality checks, no repeatable pipeline.

### Solution
A production-style **data warehouse pipeline**:

```
OpenFlights .dat files
        ↓  Extract + Transform (Python)
PostgreSQL star schema
        ↓  SQL analytics
Live dashboard (GitHub Pages)
```

### What makes this project strong
- **Real data** at scale (66k+ routes, not a toy CSV)
- **Documented design decisions** (star schema, SCD Type 2, role-playing dimensions)
- **Automated quality** (18 pytest tests, green CI badge)
- **Reproducible** (Docker + docker-compose)
- **Public demo** (live dashboard URL for CV / recruiters)

---

## 2. Complete tech stack

| Layer | Technology | Version / notes |
|-------|------------|-----------------|
| **Language** | Python | 3.11+ (3.12 locally, 3.11 in Docker/CI) |
| **Database** | PostgreSQL | 16 (Docker), 18 (local Windows) |
| **DB driver** | psycopg2-binary | ≥ 2.9.9 |
| **Config** | python-dotenv | ≥ 1.0.0 |
| **Containerisation** | Docker | Dockerfile + docker-compose |
| **Base image** | python:3.11-slim | ETL container |
| **DB image** | postgres:16-alpine | Docker Compose |
| **Testing** | pytest, pytest-cov | 18 unit tests |
| **Linting** | flake8 | CI (non-blocking) |
| **CI/CD** | GitHub Actions | Test + Docker build + Pages deploy |
| **Dashboard (live)** | HTML + Chart.js 4.4.1 | GitHub Pages (`docs/`) |
| **Dashboard (optional)** | Streamlit + pandas | Local only (`dashboard/app.py`) |
| **Pages deploy** | peaceiris/actions-gh-pages | Publishes to `gh-pages` branch |
| **Version control** | Git + GitHub | `main` branch |
| **Data format** | OpenFlights CSV-like `.dat` | `\N` = null |

### Tools used locally (not Python packages)

| Tool | Purpose |
|------|---------|
| Docker Desktop | Run Postgres + ETL in containers |
| pgAdmin / psql | Query PostgreSQL |
| Git | Source control |

---

## 3. Dependencies

### 3.1 Production ETL — `openflights-pipeline/requirements.txt`

| Package | Purpose |
|---------|---------|
| `psycopg2-binary` | PostgreSQL connection and batch inserts |
| `python-dotenv` | Load DB credentials from `.env` |

```txt
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
```

Install:
```powershell
cd openflights-pipeline
py -m pip install -r requirements.txt
```

### 3.2 Development & testing — `openflights-pipeline/requirements-dev.txt`

| Package | Purpose |
|---------|---------|
| `pytest` | Unit test runner |
| `pytest-cov` | Code coverage reports |

```txt
pytest>=8.0.0
pytest-cov>=4.1.0
```

Install:
```powershell
py -m pip install -r requirements-dev.txt
```

### 3.3 Optional Streamlit dashboard — `openflights-pipeline/dashboard/requirements.txt`

| Package | Purpose |
|---------|---------|
| `streamlit` | Local interactive dashboard |
| `pandas` | DataFrames for charts |
| `psycopg2-binary` | Live DB connection mode |
| `python-dotenv` | Environment config |

> **Note:** The public live dashboard uses static HTML on GitHub Pages — Streamlit is optional for local use only.

### 3.4 Docker images (no requirements.txt)

| Image | Packages installed |
|-------|-------------------|
| `python:3.11-slim` | From `requirements.txt` only |
| `postgres:16-alpine` | PostgreSQL server |

### 3.5 CI/CD (installed at runtime in GitHub Actions)

| Package / tool | Purpose |
|----------------|---------|
| `flake8` | Syntax / critical lint checks |
| `pytest`, `pytest-cov` | Tests + coverage |
| `codecov-action` | Upload coverage (optional) |
| Docker | Build ETL image in CI |

### 3.6 Dashboard CDN (GitHub Pages)

| Library | Source |
|---------|--------|
| Chart.js 4.4.1 | jsDelivr CDN (in `docs/index.html`) |

---

## 4. Project phases

| Phase | Deliverable | Status |
|-------|-------------|--------|
| **1** | Star schema design, `sql/schema.sql`, analytics queries | ✅ Complete |
| **2** | Python ETL, PostgreSQL load (66,316 routes) | ✅ Complete |
| **3** | Docker, pytest (18 tests), GitHub Actions CI | ✅ Complete |
| **4** | Live dashboard on GitHub Pages, portfolio docs | ✅ Complete |

---

## 5. Data sources

All files from [OpenFlights Data](https://openflights.org/data.html):

| File | Records | Maps to |
|------|---------|---------|
| `airports.dat` | 7,698 | `dim_airport` |
| `airlines.dat` | 6,162 | `dim_airline` |
| `planes.dat` | 246 | `dim_equipment` |
| `routes.dat` | 67,663 parsed → 66,316 loaded | `fact_routes` |

**Location:** `openflights-pipeline/data/`

Routes skipped during load (~449): missing foreign keys to airlines/airports not present in dimension files (normal for OpenFlights).

---

## 6. Data model (star schema)

### Architecture

```
                    dim_airport (role: source)
                           ↑
dim_airline ←── fact_routes ──→ dim_airport (role: destination)
                           ↓
                    dim_equipment

dim_date (designed for future schedule data — not populated yet)
```

### Tables

| Table | Type | Description |
|-------|------|-------------|
| `fact_routes` | Fact | One row per route: airline, src/dst airport, equipment, codeshare, stops |
| `dim_airport` | Dimension | Airport name, city, country, IATA/ICAO, lat/long, timezone |
| `dim_airline` | Dimension | Airline name, codes, country, active; SCD Type 2 columns |
| `dim_equipment` | Dimension | Aircraft IATA code, name, category |
| `dim_date` | Dimension | Calendar attributes (year, month, season, weekend) — future use |

### Key design decisions

| Decision | Rationale |
|----------|-----------|
| **Star schema** (not snowflake) | Simpler JOINs for analytics |
| **Role-playing `dim_airport`** | Same table for source and destination FKs |
| **SCD Type 2 on `dim_airline`** | `valid_from`, `valid_to`, `is_current` for future history tracking |
| **`dim_date` without route dates** | Future-proofing for schedule data |
| **Indexes on FK columns only** | Performance for JOINs without over-indexing |
| **Preserve OpenFlights IDs** | Routes reference numeric airport/airline IDs from source files |

**Schema file:** `sql/schema.sql` (also copied to `openflights-pipeline/sql/schema.sql` for Docker)

---

## 7. ETL pipeline

### Flow

```
Extract    → Read .dat files (CSV format, \N = null)
Transform  → Map columns, validate IATA/ICAO lengths, match equipment codes
Load       → Batch insert dimensions first, then facts (FK-safe)
```

### Module layout — `openflights-pipeline/etl/`

| File | Responsibility |
|------|----------------|
| `config.py` | Paths, `.env` DB settings, schema path resolution |
| `parsers.py` | Parse airports, airlines, planes, routes from `.dat` |
| `load_dimensions.py` | Load `dim_airport`, `dim_airline`, `dim_equipment` |
| `load_facts.py` | Load `fact_routes` with FK validation |
| `db.py` | Connect, drop/create schema, reset serial sequences |
| `setup_db.py` | Create `openflights_dw` database if missing |
| `run_etl.py` | CLI entry point |

### Commands

```powershell
cd openflights-pipeline

# Full load (drop tables, recreate schema, load all data)
py -m etl.run_etl --init

# Dimensions only (debugging)
py -m etl.run_etl --dimensions-only

# Create database only
py -m etl.setup_db
```

### Data quality rules (ETL)

- `\N`, `-`, empty string → SQL `NULL`
- IATA/ICAO codes wrong length → `NULL`
- Routes with missing airline/airport IDs → skipped
- Routes pointing to non-existent dimension rows → skipped

---

## 8. Dashboard

### Live dashboard (GitHub Pages) — primary

| Item | Detail |
|------|--------|
| **URL** | https://gvarun20.github.io/openflights-pipeline/ |
| **Source** | `docs/index.html` + `docs/data.json` |
| **Charts** | Chart.js — airports, countries, aircraft |
| **Deploy** | GitHub Actions → `gh-pages` branch |
| **Cost** | Free, no credit card, no localhost needed |

**GitHub Pages setup (one-time):**
1. Repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **`gh-pages`** / **`/ (root)`**
4. Save

**Refresh dashboard data after ETL:**
```powershell
cd openflights-pipeline
py dashboard/export_snapshot.py
git add docs/data.json openflights-pipeline/dashboard/demo_data.json
git commit -m "Update dashboard snapshot"
git push
```

### Optional local dashboard (Streamlit)

```powershell
cd openflights-pipeline/dashboard
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Opens http://localhost:8501 — supports demo snapshot or live PostgreSQL.

---

## 9. Docker

### Files

| File | Purpose |
|------|---------|
| `openflights-pipeline/Dockerfile` | Python 3.11 ETL image |
| `openflights-pipeline/docker-compose.yml` | Postgres + ETL orchestration |
| `openflights-pipeline/.dockerignore` | Exclude `.env`, cache, logs |

### Services

| Service | Image | Credentials |
|---------|-------|-------------|
| `postgres` | postgres:16-alpine | user: `openflights`, password: `openflights`, db: `openflights_dw` |
| `etl` | Built from Dockerfile | Connects to `postgres` hostname |

### Commands

```powershell
cd openflights-pipeline

# Run in background (recommended)
docker compose up --build -d

# Verify
docker exec openflights-postgres psql -U openflights -d openflights_dw -c "SELECT COUNT(*) FROM fact_routes;"

# Stop (keep data)
docker compose down

# Stop and delete all data
docker compose down -v
```

> **Note:** Docker Postgres and local Windows Postgres are separate environments (different credentials).

---

## 10. CI/CD (GitHub Actions)

### Workflows

| Workflow | File | Trigger | What it does |
|----------|------|---------|--------------|
| **CI Pipeline** | `.github/workflows/ci.yml` | Push / PR to `main` | pytest, flake8, Docker build |
| **Deploy Dashboard** | `.github/workflows/pages.yml` | Push to `main` | Publish `docs/` to `gh-pages` |

### CI steps
1. Checkout code
2. Python 3.11 + pip cache
3. Install `requirements.txt` + `requirements-dev.txt`
4. flake8 (critical errors only)
5. pytest with coverage (18 tests)
6. Build Docker image
7. Verify `python -m etl.run_etl --help` in container

---

## 11. Repository structure

```
openflights-pipeline/          ← GitHub repo root
├── README.md                  ← Project landing page (short)
├── DOCUMENTATION.md           ← This file (complete reference)
├── LICENSE                    ← MIT
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci.yml             ← Tests + Docker build
│       └── pages.yml          ← Dashboard deploy
├── docs/                      ← GitHub Pages dashboard
│   ├── index.html
│   └── data.json
├── sql/
│   ├── schema.sql             ← Warehouse DDL
│   └── queries.sql            ← Analytics SQL
└── openflights-pipeline/
    ├── data/                  ← Raw OpenFlights .dat files
    ├── etl/                   ← Python ETL package
    ├── dashboard/             ← Streamlit + snapshot export
    ├── tests/                 ← pytest suite
    ├── scripts/setup_db.py
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── requirements-dev.txt
    └── pytest.ini
```

---

## 12. Setup guide

### Prerequisites
- Python 3.11+ (`py` on Windows)
- PostgreSQL **or** Docker Desktop
- Git

### Option A — Docker (recommended)

```powershell
git clone https://github.com/gvarun20/openflights-pipeline.git
cd openflights-pipeline/openflights-pipeline
docker compose up --build -d
```

### Option B — Local PostgreSQL

```powershell
cd openflights-pipeline/openflights-pipeline
copy .env.example .env
# Edit .env — set DB_PASSWORD for your postgres user
py -m pip install -r requirements.txt
py scripts/setup_db.py
py -m etl.run_etl --init
```

### Verify load

```sql
SELECT COUNT(*) FROM fact_routes;  -- expect 66316
```

---

## 13. Environment variables

File: `openflights-pipeline/.env` (never commit — in `.gitignore`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `localhost` | PostgreSQL host (`postgres` in Docker) |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `openflights_dw` | Database name |
| `DB_USER` | `postgres` | Username (local) / `openflights` (Docker) |
| `DB_PASSWORD` | *(empty)* | Your PostgreSQL password |

Template: `openflights-pipeline/.env.example`

---

## 14. SQL analytics

File: `sql/queries.sql`

| # | Query type | Business question |
|---|------------|-------------------|
| 1 | CTE | Top 10 busiest airports |
| 2 | Window (`RANK`) | Airlines ranked within each country |
| 3 | Window (`SUM OVER`) | Cumulative routes per airline |
| 4 | Self-join | Bidirectional routes (A→B and B→A) |
| 5 | CTE + LEFT JOIN | Airports with no outbound routes (data quality) |
| 6 | EXPLAIN ANALYZE | Query plan / performance study |

---

## 15. Testing

```powershell
cd openflights-pipeline/openflights-pipeline
py -m pip install -r requirements-dev.txt
py -m pytest tests/ -v
```

**18 tests** covering:
- Null parsing (`\N`, empty, `-`)
- Fixed-width IATA/ICAO validation
- Boolean Y/N conversion
- Integer/float parsing
- Route record integration

Config: `openflights-pipeline/pytest.ini` (`pythonpath = .`)

---

## 16. Key metrics & insights

| Metric | Value |
|--------|------:|
| Routes loaded | 66,316 |
| Airports | 7,698 |
| Airlines | 6,162 |
| Aircraft types | 220 |
| Busiest hub | ATL (Atlanta) — 1,826 routes |
| Top country | United States — 12,832 routes |
| Most common aircraft | Airbus A320 (320) — 9,091 routes |
| Codeshare routes | 14,466 (~21.8%) |

---

## 17. Skills demonstrated

| Skill area | Evidence in this repo |
|------------|----------------------|
| Data modelling | Star schema, role-playing dims, SCD Type 2 design |
| SQL | CTEs, window functions, self-joins, EXPLAIN ANALYZE |
| Python ETL | Parsers, batch load, FK integrity, error handling |
| PostgreSQL | Schema design, indexes, 66k+ row warehouse |
| Docker | Dockerfile, multi-service compose, healthchecks |
| CI/CD | GitHub Actions, automated tests, Docker build |
| Testing | pytest unit tests, coverage |
| Analytics / BI | Live Chart.js dashboard on GitHub Pages |
| Documentation | This file, README, inline design rationale |

---

## Quick links

- **Live dashboard:** https://gvarun20.github.io/openflights-pipeline/
- **GitHub repo:** https://github.com/gvarun20/openflights-pipeline
- **CI status:** https://github.com/gvarun20/openflights-pipeline/actions
- **OpenFlights data:** https://openflights.org/data.html

---

*Last updated: June 2026*
