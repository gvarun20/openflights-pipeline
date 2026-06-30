"""Open Flights Data Warehouse — live analytics dashboard."""

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

DASHBOARD_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DASHBOARD_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DASHBOARD_DIR))

DEMO_FILE = DASHBOARD_DIR / "demo_data.json"

PHASES = [
    ("Phase 1", "Star schema design + SQL analytics", "Complete"),
    ("Phase 2", "Python ETL → PostgreSQL", "Complete"),
    ("Phase 3", "Docker + pytest + GitHub CI", "Complete"),
    ("Phase 4", "Live dashboard + portfolio polish", "In progress"),
]


def load_from_postgres() -> dict | None:
    try:
        from export_snapshot import export_snapshot

        return export_snapshot()
    except Exception as exc:
        st.sidebar.warning(f"Live DB unavailable: {exc}")
        return None


def load_demo() -> dict:
    return json.loads(DEMO_FILE.read_text(encoding="utf-8"))


st.set_page_config(
    page_title="OpenFlights Data Warehouse",
    page_icon="✈️",
    layout="wide",
)

st.title("Open Flights Data Warehouse")
st.caption("End-to-end data engineering project — ETL, star schema, Docker, CI/CD")

with st.sidebar:
    st.header("Data source")
    mode = st.radio("Connect using", ["Demo snapshot (no DB)", "Live PostgreSQL"])
    if mode.startswith("Live"):
        live = load_from_postgres()
        data = live if live else load_demo()
        if live:
            st.success("Connected to PostgreSQL")
    else:
        data = load_demo()
        st.info("Using snapshot — works without a database (Streamlit Cloud).")

    st.divider()
    st.header("Project phases")
    for phase, desc, status in PHASES:
        icon = "✅" if status == "Complete" else "🔄"
        st.markdown(f"{icon} **{phase}** — {desc}")

st.divider()

kpis = data["kpis"]
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Routes", f"{kpis['routes']:,}")
c2.metric("Airports", f"{kpis['airports']:,}")
c3.metric("Airlines", f"{kpis['airlines']:,}")
c4.metric("Aircraft types", f"{kpis['equipment']:,}")
c5.metric("Direct flights", f"{kpis['direct_routes']:,}")
c6.metric("Codeshare", f"{kpis['codeshare_routes']:,}")

st.caption(f"Snapshot date: {data.get('generated_at', 'unknown')}")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 busiest airports")
    df_airports = pd.DataFrame(data["top_airports"])
    df_airports["label"] = df_airports["iata"] + " — " + df_airports["country"]
    st.bar_chart(df_airports.set_index("label")["routes"])

with col_right:
    st.subheader("Routes by airline country (top 15)")
    df_countries = pd.DataFrame(data["routes_by_country"])
    st.bar_chart(df_countries.set_index("country")["routes"])

st.subheader("Most used aircraft types")
df_aircraft = pd.DataFrame(data["top_aircraft"])
df_aircraft["label"] = df_aircraft["code"] + " — " + df_aircraft["name"].str[:30]
st.bar_chart(df_aircraft.set_index("label")["routes"])

with st.expander("Why this project matters (for recruiters)"):
    st.markdown(
        """
        **Problem:** OpenFlights publishes raw CSV-like files — hard to analyse directly.

        **Solution:** A production-style pipeline that:
        - Models data as a **star schema** (dimensional warehouse)
        - **ETL** loads 66k+ routes with data quality checks
        - **Docker** makes it reproducible on any machine
        - **GitHub Actions** runs 18 automated tests on every push
        - **This dashboard** surfaces business insights (hub airports, fleet mix, geography)

        **Skills demonstrated:** SQL, Python, PostgreSQL, Docker, CI/CD, data modelling, analytics.
        """
    )

with st.expander("Architecture"):
    st.markdown(
        """
        ```
        OpenFlights .dat files
              ↓  Extract + Transform (Python ETL)
        PostgreSQL star schema
              ↓  SQL analytics
        Streamlit dashboard (you are here)
        ```
        """
    )
    st.markdown("[View source on GitHub](https://github.com/gvarun20/openflights-pipeline)")
