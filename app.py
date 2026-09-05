import streamlit as st
import pandas as pd
from src.profiler import profile
from src.sources import source_for, save_uploaded_file
from src.dashboard import (missing_values_chart, column_detail_grid,
                            correlation_heatmap, outlier_boxplot,
                            interactive_scatter)

st.set_page_config(page_title="AutoPilot ML X", page_icon="🤖",
                    layout="wide")
st.markdown("""
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
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-title">🤖 AutoPilot ML X</div>',
            unsafe_allow_html=True)
st.markdown("v1 of 6 · Self-Healing MLOps Platform")

page = st.sidebar.radio("Navigate", ["Dashboard", "Profiler", "About"])

if page == "Dashboard":
    st.write("Welcome to AutoPilot ML X — your async data ingestion "
             "and profiling engine.")
    st.write("Use the sidebar to upload a dataset on the **Profiler** "
             "page, or learn more on the **About** page.")

elif page == "Profiler":
    st.markdown('<div class="gradient-title" style="font-size:2rem;">'
                '📊 Data Profiler</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a dataset", type=["csv", "json", "xlsx"])

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
                "Choose a numeric column", numeric_cols)
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

elif page == "About":
    st.markdown('<div class="gradient-title" style="font-size:2rem;">'
                'ℹ️ About AutoPilot ML X</div>', unsafe_allow_html=True)
    st.write("AutoPilot ML X is the data engine of a self-healing "
             "MLOps platform — it ingests CSV/JSON/Excel files "
             "concurrently with asyncio, auto-profiles any dataset, "
             "and exposes a Flask upload API, all wrapped in a clean "
             "@pipeline decorator.")
    st.markdown("**Tech Stack:** Python · asyncio · Pandas · Flask · "
                "pytest · Streamlit")
    st.markdown("[💻 View on GitHub]"
                "(https://github.com/dharunvishnu2006-ctrl/"
                "autopilot-ml-x)")