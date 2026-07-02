"""Open Flights Data Warehouse — interactive portfolio dashboard."""

from __future__ import annotations

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
GITHUB = "https://github.com/gvarun20/openflights-pipeline"
PAGES_DASH = "https://gvarun20.github.io/openflights-pipeline/"
DOCS = f"{GITHUB}/blob/main/DOCUMENTATION.md"

PHASES = [
    ("Phase 1", "Star schema + SQL analytics", "Complete"),
    ("Phase 2", "Python ETL → PostgreSQL (66,316 routes)", "Complete"),
    ("Phase 3", "Docker + pytest + GitHub Actions CI", "Complete"),
    ("Phase 4", "GitHub Pages dashboard + documentation", "Complete"),
    ("Phase 5", "Soda data quality + integration tests", "Complete"),
    ("Phase 6", "Docker Compose profiles + batch jobs", "Complete"),
]


def _apply_streamlit_secrets() -> None:
    """Map Streamlit Cloud secrets to DB_* env vars for optional live mode."""
    import os

    try:
        secrets = st.secrets.get("postgres", {})
    except Exception:
        return
    if not secrets:
        return
    for key in ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"):
        if key in secrets:
            os.environ[key] = str(secrets[key])


def load_from_postgres() -> dict | None:
    try:
        _apply_streamlit_secrets()
        from export_snapshot import export_snapshot

        return export_snapshot()
    except Exception as exc:
        st.sidebar.warning(f"Live DB unavailable: {exc}")
        return None


def load_demo() -> dict:
    if not DEMO_FILE.exists():
        st.error(
            f"Missing `{DEMO_FILE.name}`. Run `py dashboard/export_snapshot.py` locally, "
            "then commit the updated file."
        )
        st.stop()
    return json.loads(DEMO_FILE.read_text(encoding="utf-8"))


st.set_page_config(
    page_title="OpenFlights Data Warehouse",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("✈️ Open Flights Data Warehouse")
st.caption(
    "End-to-end data engineering · PostgreSQL star schema · Python ETL · Soda quality · Docker · CI/CD"
)

with st.sidebar:
    st.header("🔗 Portfolio links")
    st.link_button("GitHub repository", GITHUB, use_container_width=True)
    st.link_button("Static dashboard (GitHub Pages)", PAGES_DASH, use_container_width=True)
    st.link_button("Full documentation", DOCS, use_container_width=True)

    st.divider()
    st.header("Data source")
    mode = st.radio(
        "Connect using",
        ["Demo snapshot (recommended on Streamlit Cloud)", "Live PostgreSQL"],
        index=0,
    )
    if mode.startswith("Live"):
        live = load_from_postgres()
        data = live if live else load_demo()
        if live:
            st.success("Connected to PostgreSQL")
        else:
            st.info("Fell back to demo snapshot.")
    else:
        data = load_demo()
        st.info("Using committed snapshot — no database required.")

    st.divider()
    st.header("Project phases")
    for phase, desc, status in PHASES:
        st.markdown(f"✅ **{phase}** — {desc}" if status == "Complete" else f"🔄 **{phase}** — {desc}")

    st.divider()
    st.caption("Built by [gvarun20](https://github.com/gvarun20) · MIT License")

kpis = data["kpis"]
top_apt = data["top_airports"][0]
top_airline = data["top_airlines"][0]
corridor = data.get("top_country_corridors", [{}])[0]

st.subheader("Key metrics")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Routes", f"{kpis['routes']:,}")
c2.metric("Airports", f"{kpis['airports']:,}")
c3.metric("Airlines", f"{kpis['airlines']:,}")
c4.metric("International", f"{data['route_scope']['International']:,}")
c5.metric("Domestic", f"{data['route_scope']['Domestic']:,}")
c6.metric(
    "Codeshare %",
    f"{100 * kpis['codeshare_routes'] / kpis['routes']:.1f}%",
)

st.caption(f"Data snapshot: **{data.get('generated_at', 'unknown')}**")

st.info(
    f"**Insights:** Busiest hub — **{top_apt['city']} ({top_apt['iata']})** with "
    f"{top_apt['routes']:,} connections · Top airline — **{top_airline['name']}** "
    f"({top_airline['routes']:,} routes) · Busiest corridor — "
    f"**{corridor.get('label', 'N/A')}** ({corridor.get('routes', 0):,} routes)."
)

tab1, tab2, tab3, tab4 = st.tabs(["Airports & airlines", "International", "Fleet", "About this project"])

with tab1:
    left, right = st.columns(2)
    with left:
        st.subheader("Top 10 busiest airports")
        df_airports = pd.DataFrame(data["top_airports"])
        df_airports["label"] = df_airports["city"] + ", " + df_airports["country"]
        st.bar_chart(df_airports.set_index("label")["routes"], height=350)
    with right:
        st.subheader("Top 10 airlines by routes")
        df_airlines = pd.DataFrame(data["top_airlines"])
        st.bar_chart(df_airlines.set_index("name")["routes"], height=350)

    st.subheader("Largest networks (unique destinations)")
    df_hubs = pd.DataFrame(data["top_network_hubs"])
    st.bar_chart(df_hubs.set_index("label")["destinations"], height=280)

with tab2:
    left, right = st.columns(2)
    with left:
        st.subheader("Domestic vs international")
        scope = pd.Series(data["route_scope"], name="routes")
        st.bar_chart(scope, height=280)
    with right:
        st.subheader("Routes by airline home country (top 15)")
        df_countries = pd.DataFrame(data["routes_by_country"])
        st.bar_chart(df_countries.set_index("country")["routes"], height=280)

    st.subheader("Top country corridors (both directions)")
    df_corridors = pd.DataFrame(data["top_country_corridors"])
    st.dataframe(
        df_corridors[["label", "routes"]].rename(columns={"label": "Corridor", "routes": "Routes"}),
        use_container_width=True,
        hide_index=True,
    )

with tab3:
    left, right = st.columns(2)
    with left:
        st.subheader("Most used aircraft types")
        df_aircraft = pd.DataFrame(data["top_aircraft"])
        df_aircraft["label"] = df_aircraft["name"].str[:36]
        st.bar_chart(df_aircraft.set_index("label")["routes"], height=350)
    with right:
        st.subheader("Codeshare vs own-operated")
        cs = pd.Series(data["codeshare_split"], name="routes")
        st.bar_chart(cs, height=350)

    st.subheader("US traffic split")
    if "us_traffic" in data:
        st.bar_chart(pd.Series(data["us_traffic"], name="routes"), height=220)

with tab4:
    st.markdown(
        f"""
        ### Problem
        [OpenFlights](https://openflights.org/data.html) publishes raw `.dat` files (~67k routes).
        They are not relational, validated, or ready for analytics.

        ### Solution
        A production-style **data warehouse pipeline**:

        ```
        .dat files  →  Python ETL  →  PostgreSQL star schema  →  Soda quality  →  Dashboards
        ```

        ### What this demonstrates
        | Skill | Evidence |
        |-------|----------|
        | Data modelling | Star schema, role-playing dimensions, SCD Type 2 design |
        | Python ETL | 66,316 routes loaded with FK validation |
        | Data quality | 8 Soda Core checks + 23 pytest tests |
        | DevOps | Docker Compose profiles, GitHub Actions CI, scheduled ETL |
        | Analytics | This app + [static dashboard]({PAGES_DASH}) |

        ### Links
        - **Repository:** [{GITHUB}]({GITHUB})
        - **Documentation:** [{DOCS}]({DOCS})
        - **CI status:** [{GITHUB}/actions]({GITHUB}/actions)
        """
    )

st.divider()
st.caption(
    "💡 Recruiters: start with the [GitHub README](%s) and [live static dashboard](%s). "
    "This Streamlit app uses the same snapshot data — no cloud database required."
    % (GITHUB, PAGES_DASH)
)
