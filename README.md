# Open Flights Data Pipeline

[![CI Pipeline](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/gvarun20/openflights-pipeline/actions/workflows/ci.yml)
[![Live Dashboard](https://img.shields.io/badge/demo-GitHub%20Pages-3b82f6?style=flat&logo=github)](https://gvarun20.github.io/openflights-pipeline/)
[![Visitor feedback](https://img.shields.io/github/issues-search/gvarun20/openflights-pipeline?query=label%3Afeedback&label=visitor%20feedback)](https://github.com/gvarun20/openflights-pipeline/issues?q=label%3Afeedback)

> **MSc portfolio demo** · 66,316 flight routes · PostgreSQL · Python ETL · free dashboard  
> *Built to show coursework skills — not a production airline system*

---

## Live demo

**Dashboard:** https://gvarun20.github.io/openflights-pipeline/ — scroll down for the **feedback box** (type your thoughts, then submit via GitHub).

**Repo:** https://github.com/gvarun20/openflights-pipeline

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
| 8 | Exported SQL metrics to JSON and built a **live dashboard** | Chart.js + Leaflet map |
| 9 | Added a **feedback form** so visitors can leave thoughts | GitHub Issues |

**Design choice:** static GitHub Pages dashboard (not Streamlit) — fast, free, and easy to share in a CV link.

**Honest scope:** demo-scale data (~66k routes), not a production airline platform.

---

## Watch the demo

**Live dashboard (works now):** [![Open live demo](https://img.shields.io/badge/▶_Open-live_dashboard-3b82f6?style=for-the-badge&logo=github)](https://gvarun20.github.io/openflights-pipeline/)

**Loom walkthrough (optional):** record ~2 min on [Loom](https://www.loom.com) (free), then replace `YOUR_LOOM_URL`:

[![Demo video](https://img.shields.io/badge/▶_Watch-Loom_demo-625DF5?style=for-the-badge&logo=loom&logoColor=white)](YOUR_LOOM_URL)

**Recording checklist (~2 min):**
1. Open the [live dashboard](https://gvarun20.github.io/openflights-pipeline/) — show map, charts, status bar (20 sec)
2. Scroll to **Feedback** — explain visitors can leave comments via GitHub (15 sec)
3. Open the [GitHub repo](https://github.com/gvarun20/openflights-pipeline) — point at green CI badge (20 sec)
4. Quick peek: `etl/`, `quality/checks.yml`, `docs/index.html` (30 sec)
5. Say it's an **MSc portfolio demo**, not live airline ops (10 sec)

**After recording:** paste your Loom share link into `README.md` where it says `YOUR_LOOM_URL`.

---

## Architecture

![Architecture diagram](docs/architecture.png)

→ Column dictionary: **[METADATA.md](METADATA.md)**  
→ Full notes: **[DOCUMENTATION.md](DOCUMENTATION.md)**

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
| Busiest hub | ATL |
| Hosting cost | £0 |

---

## Quick start

```powershell
cd openflights-pipeline
.\scripts\run_pipeline.ps1
```

**Docker:** see [DOCKER.md](openflights-pipeline/DOCKER.md)

---

## Repo extras

| File | Purpose |
|------|---------|
| [METADATA.md](METADATA.md) | What each table/column means |
| [PORTFOLIO.md](PORTFOLIO.md) | CV / LinkedIn snippets |
| [docs/GITHUB_PROFILE_README.md](docs/GITHUB_PROFILE_README.md) | GitHub profile README template |
| Issue templates | Data bug · Enhancement · Dashboard feedback |

**One-time setup (repo owner):** the **`feedback`** label is created automatically by `scripts/create_feedback_label.ps1` (or GitHub → Issues → Labels). Submit one test comment from the dashboard feedback form to verify the flow.

---

## GitHub Actions status

| Workflow | What it does |
|----------|--------------|
| **CI Pipeline** | Tests + ETL + quality + Docker — should be green |
| **Deploy Dashboard** | Pushes `docs/` to `gh-pages` branch |

**About the red badge:** If **CI Pipeline** and **Deploy Dashboard** are green, you are fine. A separate GitHub job called **"pages build and deployment"** (on the `gh-pages` branch) can fail even when the site is live — it is not your main CI. See [DOCUMENTATION.md](DOCUMENTATION.md#143-github-pages-setup-note).

---

## License

MIT — see [LICENSE](LICENSE).

*MSc demo · [gvarun20](https://github.com/gvarun20)*
