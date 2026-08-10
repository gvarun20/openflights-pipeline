# Open Flights Data Pipeline

[![CI Pipeline](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml)
[![Live Dashboard](https://img.shields.io/badge/demo-GitHub%20Pages-3b82f6?style=flat&logo=github)](https://gvarun20.github.io/openflights-pipeline/)
[![Visitor feedback](https://img.shields.io/github/issues-search/gvarun20/openflights-pipeline?query=label%3Afeedback&label=visitor%20feedback)](https://github.com/gvarun20/openflights-pipeline/issues?q=label%3Afeedback)

> **MSc portfolio demo** · 66,316 flight routes · PostgreSQL · Python ETL · free dashboard  
> *Built to show coursework skills — not a production airline system*

---

## Live demo

**Dashboard:** https://gvarun20.github.io/openflights-pipeline/

| On the dashboard | What it shows |
|------------------|---------------|
| **Status bar** | Last export time, quality passed, route count, 14 data checks |
| **Hub map** | 20 busiest airports worldwide (Leaflet + free map tiles) |
| **Charts & tables** | Airlines, corridors, aircraft, domestic vs international |
| **Feedback form** | Visitors type thoughts → submit as a GitHub Issue |

**Repo:** https://github.com/gvarun20/openflights-pipeline

---

## Documentation — where to start

| If you are… | Read this | Time |
|-------------|-----------|------|
| **Recruiter / non-technical** | This README + [live dashboard](https://gvarun20.github.io/openflights-pipeline/) | 5 min |
| **MSc reviewer / classmate** | [METADATA.md](METADATA.md) (what each table means) + [How I built this](#how-i-built-this) below | 10 min |
| **Technical interviewer** | [DOCUMENTATION.md](DOCUMENTATION.md) (full pipeline, CI, tests, quality) | 30 min |
| **CV / LinkedIn** | [PORTFOLIO.md](PORTFOLIO.md) (copy-paste snippets + demo script) | 5 min |
| **Docker / local run** | [DOCKER.md](openflights-pipeline/DOCKER.md) + [Quick start](#quick-start) below | 15 min |

---

## How I built this

A short walkthrough for recruiters and classmates — **£0 total cost**, everything runs on free tiers.

| Step | What I did | Tools |
|------|------------|-------|
| 1 | Downloaded raw OpenFlights `.dat` files | OpenFlights.org |
| 2 | Parsed messy CSV (`\N` nulls, orphan IDs) into clean rows | Python |
| 3 | Loaded a **star schema** (dims + `fact_routes`) | PostgreSQL |
| 4 | Added **14 Soda checks** so bad data fails before publish | Soda Core |
| 5 | Wrote **23 pytest tests** (unit + integration) | pytest |
| 6 | Wrapped it in **Docker Compose** for one-command runs | Docker |
| 7 | Automated test → ETL → quality → deploy in **GitHub Actions** | CI/CD |
| 8 | Exported SQL metrics to JSON and built a **live dashboard** | Chart.js + Leaflet |
| 9 | Added a **feedback form** so visitors can leave thoughts | GitHub Issues |

**Design choice:** static GitHub Pages dashboard — fast, free, and easy to share in a CV link.

**Honest scope:** demo-scale data (~66k routes), not a production airline platform.

---

## Watch the demo

**Live dashboard (works now):** [![Open live demo](https://img.shields.io/badge/▶_Open-live_dashboard-3b82f6?style=for-the-badge&logo=github)](https://gvarun20.github.io/openflights-pipeline/)

**Loom walkthrough (optional):** record ~2 min on [Loom](https://www.loom.com) (free), then replace `YOUR_LOOM_URL`:

[![Demo video](https://img.shields.io/badge/▶_Watch-Loom_demo-625DF5?style=for-the-badge&logo=loom&logoColor=white)](YOUR_LOOM_URL)

**Recording checklist (~2 min):**
1. Open the [live dashboard](https://gvarun20.github.io/openflights-pipeline/) — status bar, map, charts (20 sec)
2. Scroll to **Feedback** — explain visitors can leave comments via GitHub (15 sec)
3. Open the [GitHub repo](https://github.com/gvarun20/openflights-pipeline) — green CI badge (20 sec)
4. Quick peek: `etl/`, `quality/checks.yml`, `docs/index.html` (30 sec)
5. Say it's an **MSc portfolio demo**, not live airline ops (10 sec)

---

## Architecture

![Architecture diagram](docs/architecture.png)

→ Column dictionary: **[METADATA.md](METADATA.md)**  
→ Full technical reference: **[DOCUMENTATION.md](DOCUMENTATION.md)**

---

## What this project is

Public [OpenFlights](https://openflights.org/data.html) data → Python ETL → PostgreSQL star schema → quality checks → **GitHub Pages dashboard**.

**Demo project for my master's portfolio** — not live airline data or production infrastructure.

---

## Highlights

| | |
|---|---:|
| Routes loaded | 66,316 |
| Tests | 23 |
| Soda checks | 14 |
| Map hubs shown | 20 |
| Busiest hub | ATL |
| Hosting cost | £0 |

---

## Quick start

```powershell
cd openflights-pipeline
.\scripts\run_pipeline.ps1
```

Refresh dashboard files without a database:

```powershell
py openflights-pipeline/scripts/sync_dashboard_docs.py
```

**Docker:** see [DOCKER.md](openflights-pipeline/DOCKER.md)

---

## Repo extras

| File | Purpose |
|------|---------|
| [DOCUMENTATION.md](DOCUMENTATION.md) | Complete technical + project documentation |
| [METADATA.md](METADATA.md) | Table/column dictionary (non-technical friendly) |
| [PORTFOLIO.md](PORTFOLIO.md) | CV / LinkedIn snippets and interview script |
| [docs/GITHUB_PROFILE_README.md](docs/GITHUB_PROFILE_README.md) | GitHub profile README template |
| Issue templates | Data bug · Enhancement · Dashboard feedback |

---

## GitHub Actions

| Workflow | What it does |
|----------|--------------|
| **CI Pipeline** | Tests + ETL + 14 Soda checks + Docker |
| **Deploy Dashboard** | Publishes `docs/` to GitHub Pages |
| **Scheduled Pipeline** | Weekly ETL → export → dashboard refresh |
| **Setup dashboard feedback** | Creates `feedback` label + welcome issue (automatic) |

**About the red badge:** If **CI Pipeline** and **Deploy Dashboard** are green, you are fine. A separate **"pages build and deployment"** job on `gh-pages` can fail even when the site is live — see [DOCUMENTATION.md §14.3](DOCUMENTATION.md#143-github-pages-setup-note).

---

## License

MIT — see [LICENSE](LICENSE).

*MSc demo · [gvarun20](https://github.com/gvarun20)*
