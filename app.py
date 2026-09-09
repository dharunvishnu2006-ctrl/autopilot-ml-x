import streamlit as st
from src.profiler import profile
from src.sources import source_for, save_uploaded_file
from src.dashboard import (
    missing_values_chart,
    column_detail_grid,
    correlation_heatmap,
    outlier_boxplot,
    interactive_scatter,
)
from src.versions import (
    load_versions,
    feature_lines,
    bug_lines,
    total_roadmap_steps,
)

KNOWN_LIMITS = """
- Exact percentiles need the whole column; streaming gives
  count, sum, mean, min, max only
- The correlation heatmap caps at 15 columns and is untested
  at larger scale (current data has only 2 numeric columns)
- The LLM summary verifier checks numbers, not column names —
  a fabricated column name could pass verification
- SQLite is single-writer; fine for one profiler instance
- Date detection is heuristic and will miss unusual formats
- The concurrency test depends on generated benchmark files
  that must be created locally first
"""

st.set_page_config(page_title="AutoPilot ML X", page_icon="🤖", layout="wide")
st.markdown(
    """
<style>
.gradient-title {
    font-size: 3rem;
    font-weight: 800;
}
[data-testid="stMetric"] {
    border-radius: 12px;
    padding: 16px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="gradient-title">🤖 AutoPilot ML X</div>',
    unsafe_allow_html=True,
)
st.markdown("v1 of 6 · Self-Healing MLOps Platform")


def render_evolution():
    st.title("📈 How AutoPilot ML X Grew")
    st.caption("Every number on this page comes from versions.json")

    try:
        versions = load_versions()
    except FileNotFoundError as e:
        st.error(f"versions.json missing: {e}")
        return

    grand_total = total_roadmap_steps(versions)
    st.caption(f"Total roadmap: {grand_total} steps, {len(versions)} versions")
    cols = st.columns(len(versions))
    for i, v in enumerate(versions):
        with cols[i]:
            if v["status"] == "shipped":
                st.markdown(
                    f"<div style='background-color:{v['colour']};padding:8px;"
                    f"border-radius:6px;text-align:center;color:white;'>"
                    f"<b>{v['version']}</b><br/>{v['completion']}%<br/>"
                    f"<span style='font-size:0.75em'>"
                    f"{v['steps_covered']}/{grand_total} steps</span></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div style='border:3px dashed {v['colour']};padding:8px;"
                    f"border-radius:6px;text-align:center;color:{v['colour']};'>"
                    f"<b>{v['version']}</b><br/>{v['steps']}</div>",
                    unsafe_allow_html=True,
                )

    st.subheader("📋 Version Detail")
    for v in [x for x in versions if x["status"] == "shipped"]:
        header = (
            f"{v['version']} — {v['steps_covered']} steps, "
            f"{len(v['features'])} features, {v['tests']} tests, "
            f"{len(v['bugs_fixed'])} bugs fixed"
        )
        with st.expander(header):
            st.markdown("**Features:**")
            st.markdown("\n".join(feature_lines(v)))
            if v["bugs_fixed"]:
                st.markdown("**Bugs Fixed:**")
                st.markdown("\n".join(bug_lines(v)))

    repo = "https://github.com/dharunvishnu2006-ctrl/autopilot-ml-x/blob/main"
    st.subheader("📜 Decisions (ADRs)")
    st.markdown(
        f"- [ADR 001 — DataSource hierarchy over copied if-elif]"
        f"({repo}/docs/adr/001-datasource-hierarchy.md)\n"
        f"- [ADR 002 — SQLite over memory-only profiling]"
        f"({repo}/docs/adr/002-sqlite-over-memory.md)\n"
        f"- [ADR 003 — Threads for ingestion, chosen by measurement]"
        f"({repo}/docs/adr/003-threads-over-asyncio.md)\n"
    )

    st.subheader("⚠️ Known Limits")
    st.markdown(KNOWN_LIMITS)


page = st.sidebar.radio("Navigate", ["Dashboard", "Profiler", "Evolution", "About"])

if page == "Dashboard":
    st.write(
        "Welcome to AutoPilot ML X — your async data ingestion " "and profiling engine."
    )
    st.write(
        "Use the sidebar to upload a dataset on the **Profiler** "
        "page, or learn more on the **About** page."
    )

elif page == "Profiler":
    st.markdown(
        '<div class="gradient-title" style="font-size:2rem;">' "📊 Data Profiler</div>",
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader("Upload a dataset", type=["csv", "json", "xlsx"])

    if uploaded_file is not None:
        temp_path = save_uploaded_file(uploaded_file)
        source = source_for(temp_path)
        df = source.read()

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

        st.subheader("Missing Values per Column")
        fig1 = missing_values_chart(df)
        st.pyplot(fig1)

        st.subheader("Column Detail")
        selected_col = st.selectbox("Choose a column", df.columns)
        fig2 = column_detail_grid(df, selected_col)
        st.pyplot(fig2)

        st.subheader("Correlation Heatmap")
        fig3 = correlation_heatmap(df)
        st.pyplot(fig3)

        st.subheader("Outlier Check")
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) > 0:
            outlier_col = st.selectbox("Choose a numeric column", numeric_cols)
            fig4 = outlier_boxplot(df, outlier_col)
            st.pyplot(fig4)

        st.subheader("Interactive View")
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("X axis", numeric_cols, key="x")
            y_col = st.selectbox("Y axis", numeric_cols, key="y")
            fig5 = interactive_scatter(df, x_col, y_col)
            st.plotly_chart(fig5, use_container_width=True)

        st.subheader("Raw Report")
        st.json(report)

elif page == "Evolution":
    render_evolution()

elif page == "About":
    st.markdown(
        '<div class="gradient-title" style="font-size:2rem;">'
        "ℹ️ About AutoPilot ML X</div>",
        unsafe_allow_html=True,
    )
    st.write(
        "AutoPilot ML X is the data engine of a self-healing "
        "MLOps platform — it ingests CSV/JSON/Excel files "
        "concurrently with asyncio, auto-profiles any dataset, "
        "and exposes a Flask upload API, all wrapped in a clean "
        "@pipeline decorator."
    )
    st.markdown(
        "**Tech Stack:** Python · asyncio · Pandas · Flask · " "pytest · Streamlit"
    )
    st.markdown(
        "[💻 View on GitHub]"
        "(https://github.com/dharunvishnu2006-ctrl/"
        "autopilot-ml-x)"
    )
