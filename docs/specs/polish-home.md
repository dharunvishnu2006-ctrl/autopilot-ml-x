# AutoPilot ML X - Home page polish
# Version: v2 (no new version). Streamlit, built with Claude Code.
# Model: the AAROGYA X v1.1 Overview (brand.py, plain top, no HTML,
# Coming next in the sidebar). Updated 20 October 2026.

## Goal
Replace the two-line "Dashboard" with the family home page, built on
the v2 experiment warehouse - clearly labelled as synthetic runs.

## Tasks
1. src/brand.py: Brand(name="AutoPilot ML X", vision="Self-healing
   MLOps platform", today_text="data profiling, experiment warehouse,
   run leaderboard, pipeline DAG - synthetic runs", accent about
   #6D28D9); current_version() = newest "shipped" in
   docs/versions.json; today_line(version). "v1 of 6" goes.
2. Top of Home: st.title(name); st.markdown("#### Vision: ...");
   the Today line as st.markdown(":violet[**<today line>**]").
   Sidebar on every page: the menu, then a closed st.expander
   "Coming next - 4 modules", then the foot line
   "<name> <version> · System healthy/unhealthy".
3. Bootstrap: at first start, if data/experiment_store.db has no runs,
   build it from scripts/schema.sql and data/seed_runs.csv (about
   10,000 synthetic runs) - one function, idempotent, counts logged.
   The live demo does the same.
4. src/home_queries.py - reuse the v2 SQL (leaderboard_stats.sql,
   best_run_per_experiment.sql, read_runs.sql and the like) rather
   than new copies: kpis(), leaderboard(top=5) with n per model,
   runs_per_day(), recent_runs(n=8). The pipeline graph in
   scripts/pipeline_dag.py moves into src/ so the app can import it.
5. Home, under the top:
   Row 1 - KPI cards: Experiments - Runs - Best accuracy - Model
   types - Datasets profiled (the profiler's metadata store).
   Row 2 - (left) Leaderboard: top 5 models, mean accuracy and n.
   (right) Pipeline DAG: st.graphviz_chart of the stages - the
   structure only, no live status.
   Row 3 - Recent runs: model, status, accuracy, duration, when.
   Every run-based panel carries the caption "Synthetic runs
   (data/seed_runs.csv) - real training begins in v3".
   Coming next (the sidebar expander of task 2): Real model training
   and evaluation (v3) - MLflow registry and a model service (v4) -
   Drift detection, self-healing retraining and human-approved
   promotion (v5) - The production AI factory (v6).
6. Navigation with st.navigation: Home, Profiler, Evolution, About
   (Profiler unchanged).
7. No HTML anywhere: the gradient title and the Evolution version
   boxes are rebuilt with st.title, st.container(border=True),
   st.markdown and st.progress.
8. .streamlit/config.toml: base "light", primaryColor = the accent.
   Charts at a fixed small size, with a size test.
9. Tests: bootstrap twice gives the same counts; each KPI equals a
   query run by hand on a small fixture; leaderboard n is right;
   Today version equals versions.json; the Today line is violet bold
   Markdown; the Coming next expander is in the sidebar, closed, 4
   "arrives in" lines, no st.metric, not on Home; no
   "unsafe_allow_html" or "st.html" in any file; every page runs
   (AppTest).

## Must not
- Models in a registry, deployments, drift, pending approvals or
  "production" - none exists in v2.
- A run-based number without the "synthetic" caption.
- Any HTML; a new package; a logo or picture band.

## Verification
- Best accuracy on the card = MAX from leaderboard_stats.sql, run by
  hand in sqlite3.
- Delete data/experiment_store.db, start the app - it rebuilds.
- Laptop 1366 x 768: title lines and KPI row visible, no scrolling.
- Live demo loads at its clean address and shows the same counts.