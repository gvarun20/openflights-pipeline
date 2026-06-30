# Portfolio Guide — Impress Recruiters (No AWS / No Credit Card)

## What recruiters look for

They spend **30–60 seconds** on your GitHub. Make these visible immediately:

1. **Clear README** with architecture diagram and metrics ✅
2. **Green CI badge** — proves tests pass ✅
3. **Live demo link** — dashboard they can click without installing anything
4. **Real data** — not toy CSV with 10 rows; you have **66,316 routes**
5. **End-to-end story** — raw files → warehouse → insights

---

## Phase 4 (revised): Portfolio & Analytics — $0

Skip AWS. Do these instead:

| Step | What | Cost | Recruiter value |
|------|------|------|-----------------|
| 1 | **Streamlit dashboard** (built) | $0 | Live demo link |
| 2 | **Deploy to Streamlit Cloud** | $0, no credit card | Public URL on CV |
| 3 | **Refresh demo snapshot** after ETL | $0 | Data stays current |
| 4 | **GitHub repo polish** (README, docs) | $0 | Professional presentation |
| 5 | **Record 2-min demo video** (Loom/ OBS) | $0 | LinkedIn + CV |
| 6 | **Add GitHub topics** | $0 | Discoverability |

### Optional free upgrades (still no credit card)

| Service | Use for | Signup |
|---------|---------|--------|
| [Streamlit Cloud](https://streamlit.io/cloud) | Host dashboard | GitHub only |
| [Neon](https://neon.tech) | Free cloud PostgreSQL | Email only |
| [GitHub Pages](https://pages.github.com) | Project landing page | GitHub only |

---

## Deploy dashboard to Streamlit Cloud (15 min)

1. Push this repo to GitHub (already done)
2. Go to https://share.streamlit.io/
3. Sign in with GitHub
4. **New app** → repo: `gvarun20/openflights-pipeline`
5. **Main file path:** `openflights-pipeline/dashboard/app.py`
6. **Requirements file:** `openflights-pipeline/dashboard/requirements.txt`
7. Deploy — uses **demo snapshot** (no database needed)
8. Copy the URL → add to README and CV

Example CV line:
> Built an end-to-end aviation data warehouse (66k routes) with Python ETL, Docker, CI/CD, and a [live Streamlit dashboard](YOUR_URL).

---

## Refresh dashboard data after ETL

```powershell
cd openflights-pipeline
py -m etl.run_etl --init
py dashboard/export_snapshot.py
git add dashboard/demo_data.json
git commit -m "Update dashboard snapshot"
git push
```

Streamlit Cloud redeploys automatically on push.

---

## GitHub repo checklist

- [x] Professional README with badges
- [x] Architecture documentation
- [x] CI pipeline (green)
- [x] Tests (18 passing)
- [x] Docker support
- [x] `.gitignore` (no secrets)
- [x] Live dashboard code
- [ ] Streamlit Cloud URL in README
- [ ] 2-minute demo video
- [ ] GitHub repo description + topics: `data-engineering`, `etl`, `postgresql`, `docker`, `streamlit`, `data-warehouse`

---

## What NOT to do

- Do not commit `.env` or passwords
- Do not pay for AWS unless you choose to later
- Do not over-engineer Terraform before you have a working demo link

---

## Interview talking points

1. **Problem:** Raw OpenFlights files are not analytics-ready
2. **Modelling:** Designed star schema with documented trade-offs
3. **Pipeline:** Built idempotent ETL with FK validation and error handling
4. **Quality:** 18 automated tests + CI on every push
5. **Delivery:** Dockerised for reproducibility
6. **Impact:** Dashboard shows ATL as busiest hub, A320 as dominant aircraft — real insights
