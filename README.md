# Open Flights Data Pipeline

[![CI Pipeline](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml)
[![Live Dashboard](https://img.shields.io/badge/dashboard-live-3b82f6?style=flat&logo=github)](https://gvarun20.github.io/openflights-pipeline/)

> **66,316 flight routes** · star-schema warehouse · Python ETL · Docker · GitHub CI · live dashboard

**[📊 Live Dashboard](https://gvarun20.github.io/openflights-pipeline/)** · **[📖 Full Documentation](DOCUMENTATION.md)** · **[⚙️ CI Runs](https://github.com/gvarun20/openflights-pipeline/actions)**

---

## What this project is

An end-to-end **data engineering pipeline** that transforms raw [OpenFlights](https://openflights.org/data.html) files into a PostgreSQL data warehouse and visualises insights on a **live public dashboard** — no cloud account or credit card required.

```
.dat files  →  Python ETL  →  PostgreSQL  →  Live dashboard
                  ↑
            Docker + GitHub Actions CI
```

---

## Tech stack at a glance

| Layer | Tools |
|-------|-------|
| Database | PostgreSQL 16 |
| ETL | Python 3.11+, psycopg2 |
| Containers | Docker, docker-compose |
| Testing | pytest (18 tests) |
| CI/CD | GitHub Actions |
| Dashboard | HTML + Chart.js on GitHub Pages |

→ **[Complete tech stack, dependencies & setup guide](DOCUMENTATION.md)**

---

## Key numbers

| | |
|---|---:|
| Routes loaded | **66,316** |
| Airports | 7,698 |
| Airlines | 6,162 |
| Busiest hub | ATL — 1,826 routes |

---

## Quick start

**Docker:**
```powershell
cd openflights-pipeline
docker compose up --build -d
```

**Local Python:**
```powershell
cd openflights-pipeline
py -m pip install -r requirements.txt
py scripts/setup_db.py          # after editing .env
py -m etl.run_etl --init
```

**Tests:**
```powershell
py -m pytest tests/ -v
```

---

## Project structure

```
├── DOCUMENTATION.md       ← complete reference (start here)
├── docs/                  ← live dashboard (GitHub Pages)
├── sql/                   ← schema + analytics queries
└── openflights-pipeline/
    ├── etl/               ← Python ETL
    ├── data/              ← OpenFlights .dat files
    ├── tests/             ← pytest
    ├── Dockerfile
    └── docker-compose.yml
```

---

## License

MIT — see [LICENSE](LICENSE).
