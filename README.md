# AutoPilot ML X

Machine-learning experiment software built one version at a time: it
profiles a dataset you upload, keeps 10,000 experiment runs in a
database, ranks the models on a leaderboard, and shows the steps of a
training pipeline. Its runs are synthetic today; real model training
arrives in v3.

**Live demo:** https://autopilot-ml-x.streamlit.app
**Repository:** https://github.com/dharunvishnu2006-ctrl/autopilot-ml-x

![version](https://img.shields.io/badge/version-v2-6D28D9) ![tests](https://img.shields.io/badge/tests-182%20passed-brightgreen) ![python](https://img.shields.io/badge/python-3.14-blue)

## What it does

- Profiles a CSV, JSON or Excel file you upload: rows, columns,
  missing values and summary statistics.
- Builds its experiment warehouse at first start: 10,000 synthetic runs
  from data/seed_runs.csv, 200 experiments, 4 model types, in SQLite.
- Ranks the models on a leaderboard by mean accuracy, with the number
  of runs behind each.
- Draws the pipeline (load, clean, validate, features, train) as a
  graph - the structure only, no live status.
- Shows how the project grew, version by version, from versions.json.

## What's new in v2

v2 built roadmap steps 81-173: data structures and algorithms (a run
index, search and sort, heaps, trees, graphs, dynamic programming) and
the SQL experiment warehouse (schema, indexes, window functions, CTEs,
a trigger, full-text search, migrations), with 159 tests. The home page
polish (22 October 2026) brought the warehouse to the first screen,
labelled every run as synthetic and removed all HTML. On the way, the
tests stopped writing to the real database: each one now builds its
own.

## Run it

    pip install -r requirements.txt
    streamlit run app.py
    python scripts/make_benchmark_files.py
    pytest -q

## Numbers

| What | Value |
|---|---|
| Tests | 182 passed in 24.74 s (pytest -q, 22 Oct 2026) |
| Roadmap steps built | 173 of 600 |
| Runs in the warehouse | 10,000 synthetic, 200 experiments |
| Mean accuracy by model | 0.740 - 0.746 (synthetic) |
| Index on one query | 0.0523 s -> 0.0029 s (18x faster) |
| AVL tree height | 500 -> 11 |
| Memoized Fibonacci | 21,891 -> 39 function calls |

One index made a common query 18 times faster - the biggest single
change measured in v2.

## Known limits

The runs are synthetic: no model has been trained yet, and the Profiler
page does not save profiles, so "Datasets profiled" reads 0.
PostgreSQL setup is blocked on this Windows machine (port 5432,
permission denied), so SQLite serves the warehouse, with FTS5 and JSON1
standing in for tsvector and JSONB; Steps 155-156, 169, 170 and part of
171 are deferred. The benchmark test needs make_benchmark_files.py run
once.

## Built with

v1, v1.1 and v2 were written by hand. The test-database fix and the
home page polish were built with Claude Code and Claude: I wrote the
specs, checked the plans, ran every check, and wrote by hand the
lock-bug fix, the dependency pins, the versions.json fixes, the Coming
next format and the Evolution page test. I rejected leaving an old
conftest that pointed at the real database. Python, Streamlit, pandas,
NumPy, SQLite, SQLAlchemy, Alembic, Flask, Pydantic, pytest.

Docs: [design](docs/design.md) · [ADRs](docs/adr/) ·
[build log](docs/build_log.md) · [debugging log](docs/debugging_log.md)

## Versions

| Version | What | Tests |
|---|---|---|
| v1.0 | Foundation: async ingestion sprint | 5 |
| v1.1 | Completion: all 80 steps | 44 |
| v2 | Data structures, SQL warehouse, honest home page | 159 at release, 182 after the polish |
| v3 | Next: real model training and evaluation | |