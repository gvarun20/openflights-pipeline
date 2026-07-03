"""Open Flights Data Warehouse — MSc demo dashboard (Streamlit)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
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
    ("Phase 1", "Designed star schema + SQL queries", "Done"),
    ("Phase 2", "Built Python ETL → PostgreSQL", "Done"),
    ("Phase 3", "Docker + tests + GitHub CI", "Done"),
    ("Phase 4", "Static dashboard on GitHub Pages", "Done"),
    ("Phase 5", "Soda checks + integration tests", "Done"),
    ("Phase 6", "Docker Compose learning stack", "Done"),
]


def _apply_streamlit_secrets() -> None:
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
        st.error(f"Missing `{DEMO_FILE.name}` — run export or enrich script locally.")
        st.stop()
    return json.loads(DEMO_FILE.read_text(encoding="utf-8"))


def hub_map_figure(airports: list[dict]) -> go.Figure:
    pts = [a for a in airports if a.get("latitude") is not None]
    fig = go.Figure(
        go.Scattergeo(
            lon=[a["longitude"] for a in pts],
            lat=[a["latitude"] for a in pts],
            text=[f"{a['city']} ({a['iata']}) — {a['routes']:,} routes" for a in pts],
            mode="markers",
            marker=dict(
                size=[8 + a["routes"] / 120 for a in pts],
                color="#3b82f6",
                line=dict(width=0.5, color="white"),
            ),
        )
    )
    fig.update_layout(
        title="Top hub airports (bubble size ≈ route volume)",
        geo=dict(showland=True, landcolor="#e8e8e8", projection_type="natural earth"),
        margin=dict(l=0, r=0, t=40, b=0),
        height=480,
    )
    return fig


def route_network_figure(pairs: list[dict]) -> go.Figure:
    fig = go.Figure()
    for p in pairs:
        if not all(k in p for k in ("from_lat", "from_lon", "to_lat", "to_lon")):
            continue
        fig.add_trace(
            go.Scattergeo(
                lon=[p["from_lon"], p["to_lon"]],
                lat=[p["from_lat"], p["to_lat"]],
                mode="lines+markers",
                line=dict(width=1 + p["routes"] / 4, color="#6366f1"),
                marker=dict(size=6),
                name=f"{p['from_iata']}→{p['to_iata']}",
                hovertext=f"{p['from_city']} → {p['to_city']} ({p['routes']} routes)",
                hoverinfo="text",
            )
        )
    fig.update_layout(
        title="Sample route network (top 12 city-pairs only — demo subset)",
        geo=dict(showland=True, landcolor="#f3f4f6", projection_type="natural earth"),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        height=480,
    )
    return fig


st.set_page_config(
    page_title="OpenFlights Demo Dashboard",
    page_icon="✈️",
    layout="wide",
)

st.title("✈️ Open Flights — MSc Demo Dashboard")
st.caption(
    "Coursework-style data pipeline demo · not a production system · built to show what I learned"
)

with st.sidebar:
    st.markdown("### 🔗 Links")
    st.link_button("GitHub repo", GITHUB, use_container_width=True)
    st.link_button("Static dashboard", PAGES_DASH, use_container_width=True)
    st.link_button("Documentation", DOCS, use_container_width=True)

    st.divider()
    st.markdown("### Data")
    mode = st.radio("Source", ["Demo JSON snapshot", "Live PostgreSQL (optional)"], index=0)
    if mode.startswith("Live"):
        live = load_from_postgres()
        data = live if live else load_demo()
    else:
        data = load_demo()
        st.caption("Uses `demo_data.json` — works on Streamlit Cloud without a database.")

    st.divider()
    st.markdown("**Project phases**")
    for phase, desc, status in PHASES:
        st.markdown(f"✅ {phase}: {desc}")

st.warning(
    "**Demo note:** This is a student portfolio project using public OpenFlights data. "
    "Figures are snapshots, not live airline operations data."
)

kpis = data["kpis"]
top_apt = data["top_airports"][0]
top_airline = data["top_airlines"][0]

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Routes", f"{kpis['routes']:,}")
c2.metric("Airports", f"{kpis['airports']:,}")
c3.metric("Airlines", f"{kpis['airlines']:,}")
c4.metric("International", f"{data['route_scope']['International']:,}")
c5.metric("Domestic", f"{data['route_scope']['Domestic']:,}")
c6.metric("Codeshare %", f"{100 * kpis['codeshare_routes'] / kpis['routes']:.1f}%")
st.caption(f"Snapshot date: {data.get('generated_at', '?')}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Charts", "Map & network", "Tables", "About", "For my CV"]
)

with tab1:
    left, right = st.columns(2)
    with left:
        st.subheader("Busiest airports")
        df = pd.DataFrame(data["top_airports"])
        df["label"] = df["city"] + ", " + df["country"]
        st.bar_chart(df.set_index("label")["routes"], height=320)
    with right:
        st.subheader("Top airlines")
        st.bar_chart(pd.DataFrame(data["top_airlines"]).set_index("name")["routes"], height=320)

    left, right = st.columns(2)
    with left:
        st.subheader("Domestic vs international")
        st.bar_chart(pd.Series(data["route_scope"], name="routes"), height=260)
    with right:
        st.subheader("Top aircraft types")
        ac = pd.DataFrame(data["top_aircraft"])
        st.bar_chart(ac.set_index("name")["routes"], height=260)

with tab2:
    st.markdown(
        "Geographic views for the **demo dashboard** — only top hubs / top route pairs are drawn "
        "(drawing all 66k routes would melt the browser)."
    )
    left, right = st.columns(2)
    with left:
        st.plotly_chart(hub_map_figure(data["top_airports"]), use_container_width=True)
    with right:
        st.plotly_chart(route_network_figure(data["top_route_pairs"]), use_container_width=True)

    map_rows = [
        {
            "lat": a["latitude"],
            "lon": a["longitude"],
            "size": a["routes"] / 100,
        }
        for a in data["top_airports"]
        if a.get("latitude") is not None
    ]
    if map_rows:
        st.subheader("Simple map (Streamlit built-in)")
        st.map(pd.DataFrame(map_rows), latitude="lat", longitude="lon", size="size")

with tab3:
    st.subheader("Country corridors")
    st.dataframe(pd.DataFrame(data["top_country_corridors"]), use_container_width=True, hide_index=True)
    st.subheader("Busiest city-pair routes")
    st.dataframe(pd.DataFrame(data["top_route_pairs"]), use_container_width=True, hide_index=True)

with tab4:
    st.markdown(
        f"""
        ### What is this?
        A **master's-level demo project** showing I can take messy open data and turn it into
        something queryable and visual.

        ### Pipeline (simplified)
        ```
        OpenFlights .dat  →  Python ETL  →  PostgreSQL  →  checks  →  dashboards
        ```

        ### What I intentionally did *not* build
        - Real-time flight tracking
        - Production SLAs / on-call
        - Paid cloud infra (everything is free-tier friendly)

        ### Links
        - Repo: [{GITHUB}]({GITHUB})
        - Metadata dictionary: [METADATA.md]({GITHUB}/blob/main/METADATA.md)
        - Full write-up: [DOCUMENTATION.md]({DOCS})
        """
    )

with tab5:
    st.markdown(
        """
        ### Copy-paste for applications

        > Built a demo data warehouse pipeline (OpenFlights, 66k routes) with Python ETL,
        > PostgreSQL star schema, Soda data quality checks, Docker, and GitHub Actions CI.
        > Published interactive dashboards on GitHub Pages and Streamlit.

        ### Skills this project is meant to show
        - SQL & dimensional modelling
        - Python ETL scripting
        - Basic data quality automation
        - Git + CI habits
        - Dashboarding for non-technical viewers

        ### Honest limitations (good to mention in interviews)
        - Batch-only, not streaming
        - OpenFlights data is incomplete/outdated in places
        - Quality checks are rule-based, not ML anomaly detection
        """
    )

st.caption("MSc portfolio demo · MIT License · [gvarun20](https://github.com/gvarun20)")
