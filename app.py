import streamlit as st
import pandas as pd
from src.profiler import profile
import random
import altair as alt

st.set_page_config(page_title="AutoPilot ML X", page_icon="🤖", layout="wide")
st.markdown("""
<style>
.gradient-title {
    font-size: 3rem;             /* keep the size, drop the colour */
    font-weight: 800;            /* keep the weight */
}
[data-testid="stMetric"] {
    border-radius: 12px;         /* keep the shape */
    padding: 16px;               /* keep the spacing */
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-title">🤖 AutoPilot ML X</div>', unsafe_allow_html=True)
st.markdown("v1 of 6 · Self-Healing MLOps Platform")

stars_html = ""
for i in range(18):
    top = random.randint(0, 800)
    left = random.randint(0, 1800)
    delay = random.uniform(0, 2)
    stars_html += f'<div class="star" style="top:{top}px; left:{left}px; animation-delay:{delay}s;"></div>'

st.markdown(stars_html, unsafe_allow_html=True)
page = st.sidebar.radio("Navigate", ["Dashboard", "Profiler", "About"])

if page == "Dashboard":
    st.write("Welcome to AutoPilot ML X — your async data ingestion and profiling engine.")
    st.write("Use the sidebar to upload a dataset on the **Profiler** page, or learn more on the **About** page.")
elif page == "Profiler":
    st.markdown('<div class="gradient-title" style="font-size:2rem;">📊 Data Profiler</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a dataset", type=["csv", "json", "xlsx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write(df.head())
        report = profile(df)
        total_missing = sum(report["missing_values"].values())

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files Ingested", 1)
        with col2:
            st.metric("Rows Profiled", report["rows"])
        with col3:
            st.metric("Missing Values Found", total_missing)

        st.json(report)
        missing_df = pd.DataFrame({
            "column": list(report["missing_values"].keys()),
            "missing_count": list(report["missing_values"].values())
        })

        chart = alt.Chart(missing_df).mark_bar().encode(
            x="column",
            y="missing_count"
        )

        st.altair_chart(chart, use_container_width=True)
elif page == "About":
    st.markdown('<div class="gradient-title" style="font-size:2rem;">ℹ️ About AutoPilot ML X</div>', unsafe_allow_html=True)
    st.write("AutoPilot ML X is the data engine of a self-healing MLOps platform — it ingests CSV/JSON/Excel files concurrently with asyncio, auto-profiles any dataset, and exposes a Flask upload API, all wrapped in a clean @pipeline decorator.")
    st.markdown("**Tech Stack:** Python · asyncio · Pandas · Flask · pytest · Streamlit")
    st.markdown("[💻 View on GitHub](https://github.com/dharunvishnu2006-ctrl/autopilot-ml-x)")