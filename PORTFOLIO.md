# Portfolio Guide — Open Flights Data Pipeline

Use this when preparing your **CV, LinkedIn, GitHub profile, and interviews**.

---

## Elevator pitch (30 seconds)

> I built a demo data engineering pipeline that loads 66,000+ flight routes from OpenFlights into a PostgreSQL star-schema warehouse. It includes Python ETL, 14 Soda data quality checks, 23 automated tests, Docker Compose, GitHub Actions CI, a live dashboard with an interactive hub map, and a visitor feedback form — all hosted for free on GitHub Pages.

---

## Links for your CV

| Link | URL |
|------|-----|
| **GitHub repository** | https://github.com/gvarun20/openflights-pipeline |
| **Live dashboard** | https://gvarun20.github.io/openflights-pipeline/ |
| **Documentation** | https://github.com/gvarun20/openflights-pipeline/blob/main/DOCUMENTATION.md |
| **CI** | https://github.com/gvarun20/openflights-pipeline/actions |
| **Visitor feedback** | https://github.com/gvarun20/openflights-pipeline/issues?q=label%3Afeedback |

**CV one-liner:**

> Open Flights Data Pipeline — Python ETL, PostgreSQL, Soda, Docker, GitHub Actions · [GitHub](https://github.com/gvarun20/openflights-pipeline) · [Dashboard](https://gvarun20.github.io/openflights-pipeline/)

---

## GitHub checklist

| Field | Value |
|-------|-------|
| **Description** | MSc demo: OpenFlights → PostgreSQL → Soda → GitHub Pages dashboard + hub map |
| **Website** | https://gvarun20.github.io/openflights-pipeline/ |
| **Topics** | `data-engineering` `postgresql` `python` `etl` `docker` `github-actions` `data-quality` `portfolio` |
| **Pin repo** | Yes — on your profile |
| **`feedback` label** | Create once (Issues → Labels) or run `scripts/create_feedback_label.ps1` |
| **Loom video** | Record 2 min demo, paste link in README |

---

## LinkedIn template

Built a demo data warehouse pipeline (66,316 routes) with Python ETL, PostgreSQL star schema, 14 Soda checks, Docker, GitHub Actions CI, and a public dashboard (Chart.js + Leaflet map). Visitors can leave feedback via GitHub Issues.

**Skills:** Python, SQL, PostgreSQL, ETL, Docker, GitHub Actions, Data Quality

---

## 2-minute Loom script

| Time | Show | Say |
|------|------|-----|
| 0:00–0:20 | Live dashboard — status bar, KPIs | “66k routes from OpenFlights in a star schema” |
| 0:20–0:40 | Scroll to **hub map** and charts | “Free GitHub Pages — map uses Leaflet + OpenStreetMap” |
| 0:40–0:55 | **Feedback** box at bottom | “Visitors can leave thoughts — stored as GitHub Issues” |
| 0:55–1:15 | GitHub repo + green **CI Pipeline** badge | “23 tests + 14 Soda checks on every push” |
| 1:15–1:45 | Quick code: `etl/`, `quality/checks.yml` | “Python ETL, quality gates before dashboard publish” |
| 1:45–2:00 | Back to README / architecture diagram | “MSc portfolio demo — not production airline data” |

---

## Interview talking points

- **Why star schema?** Simpler joins for BI; dims for airports/airlines/equipment.
- **Why Soda?** Declarative checks in CI — row counts, nulls, coordinate bounds.
- **Why static dashboard?** Zero hosting cost; good enough for portfolio storytelling.
- **What would you add next?** dbt marts, Prefect orchestration, or cloud Postgres (if budget allowed).

---

*Last updated: August 2026*
