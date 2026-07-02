# Portfolio Guide — Open Flights Data Pipeline

Use this page when preparing your **CV, LinkedIn, GitHub profile, and interviews**.

---

## Elevator pitch (30 seconds)

> I built an end-to-end data engineering pipeline that loads 66,000+ flight routes from OpenFlights into a PostgreSQL star-schema warehouse. The project includes Python ETL, Soda Core data quality checks, 23 automated tests, Docker Compose, GitHub Actions CI with a weekly scheduled refresh, and two public dashboards — so anyone can explore the results without running the code.

---

## Links to put on your CV

Replace the Streamlit URL after you deploy (see [STREAMLIT_CLOUD.md](openflights-pipeline/dashboard/STREAMLIT_CLOUD.md)).

| Link | URL |
|------|-----|
| **GitHub repository** | https://github.com/gvarun20/openflights-pipeline |
| **Static dashboard** | https://gvarun20.github.io/openflights-pipeline/ |
| **Streamlit dashboard** | *Deploy → paste URL here* |
| **Documentation** | https://github.com/gvarun20/openflights-pipeline/blob/main/DOCUMENTATION.md |
| **CI (green badge)** | https://github.com/gvarun20/openflights-pipeline/actions |

**CV one-liner example:**

> Open Flights Data Pipeline — Python ETL, PostgreSQL, Soda, Docker, GitHub Actions · [GitHub](https://github.com/gvarun20/openflights-pipeline) · [Dashboard](https://gvarun20.github.io/openflights-pipeline/)

---

## GitHub repository checklist

Do these on https://github.com/gvarun20/openflights-pipeline:

### About section (top right of repo page)

| Field | Suggested value |
|-------|-----------------|
| **Description** | End-to-end data warehouse pipeline: OpenFlights → PostgreSQL → Soda quality → live dashboards |
| **Website** | https://gvarun20.github.io/openflights-pipeline/ *(add Streamlit URL too in README)* |
| **Topics** | `data-engineering` `postgresql` `python` `etl` `docker` `streamlit` `github-actions` `data-quality` `star-schema` `portfolio` |

### Pin the repository

1. Go to your GitHub profile → **Customize your pins**
2. Pin **openflights-pipeline**

### README first impression

Your README already includes:
- CI badges
- Live dashboard link
- Architecture diagram
- Key metrics (66,316 routes)
- Tech stack table

After Streamlit deploy, add the Streamlit badge (see README update).

---

## LinkedIn project entry (copy-paste template)

**Title:** Open Flights Data Warehouse Pipeline

**Description:**

Built a production-style data engineering pipeline processing 66,316 aviation routes from raw OpenFlights files into a PostgreSQL star-schema warehouse.

- Designed star schema with role-playing dimensions and SCD Type 2 airline history
- Implemented Python ETL with FK validation and batch loading
- Added Soda Core data quality checks (8 rules) and 23 pytest tests
- Containerised with Docker Compose (profiles for dev, pipeline, test)
- Automated CI/CD with GitHub Actions + weekly scheduled ETL refresh
- Published interactive dashboards on GitHub Pages and Streamlit Cloud

**Skills:** Python, SQL, PostgreSQL, ETL, Docker, GitHub Actions, Data Quality, Streamlit

**Links:** [GitHub] [Dashboard]

---

## Interview talking points

| Topic | What to say |
|-------|-------------|
| **Why star schema?** | Faster analytics JOINs; airports play two roles (source/destination) |
| **Data quality** | Soda checks row counts and null FKs; integration tests assert ATL is top hub |
| **Why routes skipped?** | ~449 routes had orphan FKs — rejected rather than corrupting the warehouse |
| **CI pipeline** | Unit tests → ETL → Soda → integration tests → Docker compose test |
| **Why two dashboards?** | GitHub Pages = always-on static; Streamlit = interactive portfolio demo |
| **Production next steps** | Prefect orchestration, cloud Postgres, Grafana monitoring (see README) |

---

## Demo script (2 minutes for screen share)

1. **GitHub repo** (15 sec) — README, badges, architecture diagram
2. **Static dashboard** (30 sec) — KPIs, corridors, top airports
3. **Streamlit app** (30 sec) — tabs, insights, about section
4. **Code walkthrough** (30 sec) — `etl/run_etl.py`, `quality/checks.yml`, `docker-compose.yml`
5. **CI** (15 sec) — green Actions tab, show test + ETL steps

---

## Optional extras (when you have time)

| Enhancement | Impact |
|-------------|--------|
| 60–90 sec Loom video | Embed link in README |
| GitHub profile README | Link pinned project |
| Blog post on Medium/Dev.to | SEO + credibility |
| Schema diagram PNG in README | Visual for non-technical recruiters |

---

*Last updated: June 2026*
