import sqlite3
from contextlib import closing
from pathlib import Path

import streamlit as st
from src.bootstrap import ensure_store, store_path
from src.brand import (
    BRAND,
    COMING_NEXT,
    coming_next_lines,
    current_version,
    foot_line,
    today_line,
)
from src.home_queries import (
    kpis,
    leaderboard,
    recent_runs,
    system_healthy,
)
from src.pipeline_dag import home_pipeline, to_dot
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

SYNTHETIC = " - ".join(
    [
        "Synthetic runs (data/seed_runs.csv)",
        "real training begins in v3",
    ]
)
DAG_WIDTH = 360

st.set_page_config(page_title=BRAND.name, page_icon="🤖", layout="wide")


@st.cache_resource
def load_store(path: str) -> dict:
    # Build experiment store once
    return ensure_store(Path(path))


def store_ready() -> bool:
    # Bootstrap store, report any failure
    try:
        load_store(str(store_path()))
    except (sqlite3.Error, OSError) as e:
        st.error(f"Experiment store unavailable: {e}")
        return False
    return True


def render_home():
    version = current_version()
    st.title(BRAND.name)
    st.markdown(f"#### Vision: {BRAND.vision}")
    st.markdown(f":violet[**{today_line(version)}**]")

    if not store_ready():
        return
    with closing(sqlite3.connect(store_path())) as conn:
        k = kpis(conn)
        board = leaderboard(conn, top=5)
        recent = recent_runs(conn, n=8)

    best = k["best_accuracy"]
    cards = [
        ("Experiments", f"{k['experiments']:,}"),
        ("Runs", f"{k['runs']:,}"),
        ("Best accuracy", "—" if best is None else f"{best:.3f}"),
        ("Model types", f"{k['model_types']:,}"),
        ("Datasets profiled", f"{k['datasets_profiled']:,}"),
    ]
    for col, (label, value) in zip(st.columns(len(cards)), cards):
        col.metric(label, value, border=True)
    st.caption(SYNTHETIC)
    if k["datasets_profiled"] == 0:
        st.caption(
            "Datasets profiled is 0: no dataset has been profiled "
            f"yet - the Profiler page does not save profiles in "
            f"{version}."
        )

    left, right = st.columns(2)
    with left:
        st.subheader("Leaderboard")
        st.dataframe(
            board,
            hide_index=True,
            column_config={
                "model": "Model",
                "mean_accuracy": st.column_config.NumberColumn(
                    "Mean accuracy", format="%.3f"
                ),
                "n": "n",
            },
        )
        st.caption(SYNTHETIC)
    with right:
        st.subheader("Pipeline DAG")
        st.graphviz_chart(to_dot(home_pipeline()), width=DAG_WIDTH)
        st.caption("Pipeline stages - structure only, no live status")

    st.subheader("Recent runs")
    acc = st.column_config.NumberColumn("Accuracy", format="%.3f")
    dur = st.column_config.NumberColumn("Duration (s)", format="%.1f")
    st.dataframe(
        recent,
        hide_index=True,
        column_config={
            "model": "Model",
            "status": "Status",
            "accuracy": acc,
            "duration": dur,
            "started_at": "When",
        },
    )
    st.caption(SYNTHETIC)


def render_profiler():
    st.title("📊 Data Profiler")
    uploaded_file = st.file_uploader(
        "Upload a dataset",
        type=["csv", "json", "xlsx"],
    )

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
            outlier_col = st.selectbox(
                "Choose a numeric column",
                numeric_cols,
            )
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
        with cols[i], st.container(border=True):
            if v["status"] == "shipped":
                st.markdown(f"**{v['version']}**")
                st.progress(
                    v["completion"] / 100,
                    text=f"{v['completion']}%",
                )
                st.caption(f"{v['steps_covered']}/{grand_total} steps")
            else:
                st.markdown(f"**{v['version']}** · planned")
                st.caption(f"steps {v['steps']}")

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
        f"- [ADR 006 — Destructive migration downgrades]"
        f"({repo}/docs/adr/006-migration-downgrade-data-loss.md)\n"
        f"- [ADR 007 — Trigger vs application-level update]"
        f"({repo}/docs/adr/007-trigger-vs-application-update.md)\n"
        f"- [ADR 008 — SQLite workaround vs blocking on PostgreSQL]"
        f"({repo}/docs/adr/008-sqlite-workaround-vs-blocking.md)\n"
    )

    st.subheader("⚠️ Known Limits")
    st.markdown(KNOWN_LIMITS)


def render_about():
    st.title("ℹ️ About AutoPilot ML X")
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


def is_healthy() -> bool:
    # Check store has runs now
    if not store_ready():
        return False
    with closing(sqlite3.connect(store_path())) as conn:
        return system_healthy(conn)


def render_sidebar():
    # Draw expander and foot line
    with st.sidebar:
        label = f"Coming next - {len(COMING_NEXT)} modules"
        with st.expander(label, expanded=False):
            st.markdown("\n".join(coming_next_lines()))
        st.caption(foot_line(current_version(), is_healthy()))


def main():
    # Build menu, sidebar, run page
    pg = st.navigation(
        [
            st.Page(render_home, title="Home", icon="🏠", default=True),
            st.Page(render_profiler, title="Profiler", url_path="profiler"),
            st.Page(
                render_evolution,
                title="Evolution",
                url_path="evolution",
            ),
            st.Page(render_about, title="About", url_path="about"),
        ],
        position="sidebar",
    )
    render_sidebar()
    pg.run()


if __name__ == "__main__":
    main()
