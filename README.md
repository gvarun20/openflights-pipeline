# Open Flights Data Pipeline

[![CI Pipeline](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml)

> End-to-end **data engineering** project: raw OpenFlights files → star-schema warehouse → automated ETL → Docker → CI/CD → **live analytics dashboard**.

**Author:** Varun G · [GitHub](https://github.com/gvarun20/openflights-pipeline)

---

## What this project does (30-second pitch)

OpenFlights publishes messy `.dat` files with 67k+ flight routes. This project turns them into a **queryable PostgreSQL data warehouse** using a **star schema**, loads them with a **Python ETL pipeline**, packages everything in **Docker**, tests automatically with **GitHub Actions**, and visualises insights in a **Streamlit dashboard**.

**Why it matters:** This mirrors how real data teams work — model → extract → transform → load → test → deploy → analyse.

---

## Live demo

| Demo | How to view |
|------|-------------|
| **Dashboard (local)** | `cd openflights-pipeline/dashboard && py -m streamlit run app.py` |
| **Dashboard (cloud, free)** | Deploy to [Streamlit Community Cloud](https://streamlit.io/cloud) — no credit card, GitHub login only |
| **CI pipeline** | [GitHub Actions runs](https://github.com/gvarun20/openflights-pipeline/actions) |

---

## Key metrics (from warehouse)

| Metric | Value |
|--------|------:|
| Flight routes loaded | **66,316** |
| Airports | 7,698 |
| Airlines | 6,162 |
| Busiest hub | ATL (Atlanta) — 1,826 routes |
| Top aircraft | Airbus A320 — 9,091 routes |

---

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│  .dat files │ ──► │  Python ETL  │ ──► │  PostgreSQL     │ ──► │  Streamlit   │
│  (OpenFlights)    │  (extract/   │     │  star schema    │     │  dashboard   │
└─────────────┘     │   transform) │     └─────────────────┘     └──────────────┘
                    └──────────────┘              ▲
                           ▲                      │
                    ┌──────┴──────┐        ┌──────┴──────┐
                    │   Docker    │        │  SQL analytics │
                    │   compose   │        │  (CTEs, windows)│
                    └─────────────┘        └───────────────┘
                           ▲
                    ┌──────┴──────┐
                    │ GitHub Actions │  18 tests on every push
                    └─────────────┘
```

Full design notes: [docs/ARCHITECTURE.md](openflights-pipeline/docs/ARCHITECTURE.md)

---

## Tech stack

| Layer | Tools |
|-------|-------|
| Data source | OpenFlights `.dat` files |
| Modelling | Star schema (fact + dimensions, SCD Type 2 ready) |
| Database | PostgreSQL 16/18 |
| ETL | Python 3.11+, psycopg2 |
| Containerisation | Docker, docker-compose |
| Testing | pytest (18 tests), flake8 |
| CI/CD | GitHub Actions |
| Visualisation | Streamlit, pandas |

---

## Project phases

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 1 | Star schema + SQL analytics | ✅ |
| 2 | Python ETL → PostgreSQL | ✅ |
| 3 | Docker + GitHub CI (green badge) | ✅ |
| 4 | Live dashboard + portfolio polish | ✅ |

---

## Quick start

### Run ETL (Docker — recommended)

```powershell
cd openflights-pipeline
docker compose up --build -d
docker exec openflights-postgres psql -U openflights -d openflights_dw -c "SELECT COUNT(*) FROM fact_routes;"
```

### Run ETL (local Python)

```powershell
cd openflights-pipeline
py -m pip install -r requirements.txt
# Edit .env with your PostgreSQL password
py scripts/setup_db.py
py -m etl.run_etl --init
```

### Run dashboard

```powershell
cd openflights-pipeline/dashboard
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Opens at http://localhost:8501 — works in **demo mode** without PostgreSQL.

### Run tests

```powershell
cd openflights-pipeline
py -m pip install -r requirements-dev.txt
py -m pytest tests/ -v
```

---

## Repository structure

```
├── sql/                          # Schema + analytics SQL
├── openflights-pipeline/
│   ├── data/                     # Raw OpenFlights files
│   ├── etl/                      # Python ETL package
│   ├── dashboard/                # Streamlit live dashboard
│   ├── tests/                    # pytest suite
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/workflows/ci.yml      # Automated CI
└── README.md                     # You are here
```

---

## Skills demonstrated (for recruiters)

- **Data modelling** — star schema, role-playing dimensions, SCD Type 2 design
- **SQL** — CTEs, window functions, self-joins, EXPLAIN ANALYZE
- **Python ETL** — parsing, validation, batch loading, FK integrity
- **DevOps** — Docker, docker-compose, GitHub Actions CI/CD
- **Testing** — unit tests with pytest + coverage
- **Analytics** — interactive dashboard with real aviation insights

---

## Documentation

- [Detailed README](openflights-pipeline/docs/README.md)
- [Architecture & design decisions](openflights-pipeline/docs/ARCHITECTURE.md)
- [Portfolio guide (no AWS needed)](openflights-pipeline/docs/PORTFOLIO.md)

---

## License

MIT — see [LICENSE](LICENSE).
