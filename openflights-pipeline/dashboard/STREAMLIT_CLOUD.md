# Streamlit Community Cloud — Deploy Guide

Deploy the interactive dashboard for **free** (no credit card). It uses the committed `demo_data.json` snapshot — PostgreSQL is optional.

---

## Before you deploy

1. Push the latest code to GitHub: `https://github.com/gvarun20/openflights-pipeline`
2. Confirm `openflights-pipeline/dashboard/demo_data.json` exists in the repo (it should).

---

## Step-by-step deployment

### 1. Sign in to Streamlit Cloud

Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with your **GitHub account** (`gvarun20`).

### 2. Create a new app

Click **New app** and fill in:

| Field | Value |
|-------|-------|
| **Repository** | `gvarun20/openflights-pipeline` |
| **Branch** | `main` |
| **Main file path** | `openflights-pipeline/dashboard/app.py` |

Streamlit auto-detects `openflights-pipeline/dashboard/requirements.txt`.

### 3. Advanced settings (optional)

| Setting | Value |
|---------|-------|
| Python version | **3.11** |
| App URL slug | e.g. `openflights-pipeline` |

Your app URL will look like:

```
https://openflights-pipeline.streamlit.app
```

(or similar — you choose the slug during setup)

### 4. Deploy

Click **Deploy**. First build takes 2–5 minutes.

### 5. Verify

- App loads without errors
- Sidebar shows **Demo snapshot** mode
- KPIs show **66,316** routes
- Tabs show charts (airports, airlines, corridors)

---

## After deployment — add URL everywhere

| Place | What to add |
|-------|-------------|
| **GitHub README** | Streamlit badge + link (update `STREAMLIT_APP_URL` in README after deploy) |
| **GitHub repo About** | Website field → Streamlit URL |
| **CV / LinkedIn** | Both dashboard links |
| **GitHub profile pin** | Pin this repository |

---

## Optional: Live PostgreSQL on Streamlit Cloud

By default the app uses **demo snapshot** (no DB needed). To connect a cloud Postgres (Neon, Supabase free tier, etc.):

1. Streamlit app → **Settings** → **Secrets**
2. Add:

```toml
[postgres]
DB_HOST = "your-host.neon.tech"
DB_PORT = "5432"
DB_NAME = "openflights_dw"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
```

3. In the app sidebar, select **Live PostgreSQL**

> For portfolio purposes, **demo mode is enough**. Recruiters do not need live DB access.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: etl` | Main file path must be `openflights-pipeline/dashboard/app.py`; requirements in `dashboard/` |
| Missing demo data | Run `py dashboard/export_snapshot.py` locally, commit `demo_data.json`, redeploy |
| Build fails on psycopg2 | Requirements include `psycopg2-binary`; use Python 3.11 in advanced settings |
| App shows old numbers | Re-export snapshot, push to GitHub, reboot app in Streamlit settings |

---

## Redeploy after code changes

Streamlit Cloud redeploys automatically when you push to `main`. You can also click **Reboot app** in the Streamlit admin panel.

---

*See also: [PORTFOLIO.md](../PORTFOLIO.md) for CV and GitHub profile checklist.*
