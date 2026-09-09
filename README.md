# 🤖 AutoPilot ML X v1.1 — Async Data Ingestion & Profiling Engine

**The data engine of a self-healing MLOps platform.** Ingests CSV/JSON/Excel concurrently, auto-profiles any dataset, and exposes a Flask API — all wrapped in a clean `@pipeline` decorator.

![Python](https://img.shields.io/badge/Python-3.14-blue) ![asyncio](https://img.shields.io/badge/asyncio-concurrent-purple) ![Pandas](https://img.shields.io/badge/Pandas-data-orange) ![NumPy](https://img.shields.io/badge/NumPy-vectorised-blue) ![Flask](https://img.shields.io/badge/Flask-API-green) ![pytest](https://img.shields.io/badge/pytest-32%20passing-brightgreen) ![mypy](https://img.shields.io/badge/mypy-clean-blue) ![bandit](https://img.shields.io/badge/bandit-clean-yellow) ![Streamlit](https://img.shields.io/badge/Streamlit-deployed-red)

🔗 **Live demo:** https://autopilot-ml-x-v1-gprhnmfn2nhiemmsu8c6dp.streamlit.app/

## 📖 The Honest Story

The audit showed that only 28 of the 80 planned steps were actually completed, and the original concurrency claim was also wrong. I tested the implementation, found the gaps, and fixed the concurrency issue instead of leaving the README claim unsupported.

Full details, real measured numbers, and all trade-offs are in [`docs/design.md`](docs/design.md) and the [ADRs](docs/adr/).

## ✨ Features

**v1.0 (shipped):**
- **Async Data Ingestion** — reads CSV/JSON/Excel files using `asyncio.gather`
- **Data Profiler** — auto-generates shape, dtypes, missing values, and statistical summary for any dataset
- **`@pipeline` Decorator** — clean, automatic START/DONE logging with timing for any function
- **Flask Upload API** — `/upload` endpoint validates files and returns the profile report as JSON
- **OOP Ingestor** — `AutoPilotIngestor` class ties ingestion + profiling into one clean, reusable interface

**v1.1 additions (E1–E15):**
- **E1** Typed Dataset Records — `IngestResult`, `DatasetSchema`
- **E2** Structured Logging + Text Cleaning — JSON logs, date detection, regex cleaning
- **E3** The Metadata Store — SQLite profile history, foreign keys enforced
- **E4** Python Craft — five classic traps reproduced and fixed
- **E5** The DataSource Hierarchy — one polymorphic reader, one factory
- **E6** Decorators, Context Managers, Caching — `@lru_cache`, proven rollback safety
- **E7** Streaming Large Datasets — generators, 31x less peak memory
- **E8** Concurrency Measured — the async claim disproven, threads win at 1.46x
- **E9** NumPy Vectorised Profiling — 146.5x speedup over a loop
- **E10** Pandas Deep Profiling — grouped stats, outer-join change reports
- **E11** The Real Dashboard — Matplotlib/Seaborn/Plotly, theme-aware
- **E12** External Data Enrichment — SHA256 fingerprinting, retry/backoff, `.env` secrets
- **E13** Engineering Discipline — pre-commit (black/flake8/mypy/bandit), real PR cycle
- **E14** LLM-Assisted Profile Summaries — verified against hallucination
- **E15** Consolidation — packaging, documentation, this README

## 📊 Measured Results

| Metric | Result |
|---|---|
| Concurrency: shipped "async" vs threads | 1.5s → 1.0s (**1.46x** real speedup) |
| Streaming vs whole-file memory (92MB file) | 275.3MB → 8.9MB (**31x** less) |
| NumPy vectorised vs loop (1M values) | 133.92ms → 0.91ms (**146.5x**) |
| SHA256 fingerprint (92MB file) | 0.165s |
| flake8 findings | 21 → 0 |
| mypy errors | 7 → 0 |
| bandit findings | 62 → 0 |
| Tests | 5 (v1.0) → **32** (v1.1) |

Full tables and trade-offs: [`docs/design.md`](docs/design.md)

## 🏗️ Architecture

Files → `source_for()` factory → polymorphic `DataSource` reader → `@pipeline`-wrapped profiler → SQLite (`runs` / `datasets` / `column_stats`) → dashboard / API.

*A generated architecture diagram is a known gap in this version — tracked as a follow-up rather than hand-drawn, to keep every diagram in this project generated from code, not illustrated after the fact.*

## 🛠️ Tech Stack

Python 3.14 · asyncio · Pandas · NumPy · Matplotlib · Seaborn · Plotly · Flask · SQLite · Pydantic · pytest · Streamlit · pre-commit (black, flake8, mypy, bandit)

## 🚀 How to Run

```bash
git clone https://github.com/dharunvishnu2006-ctrl/autopilot-ml-x.git
cd autopilot-ml-x
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Run the full quality gate:
```bash
bash scripts/check.sh
```

## 📚 What I Learned

I learned that testing and measuring can reveal problems that aren't obvious from the code. The async issue and fake-passing test especially taught me to question assumptions and verify behavior.

## 🗺️ Roadmap

v1.1 of 6 — Layer 1 (the data foundation) is complete: 80/80 steps.
Next: **v2** adds data structures and SQL (steps 81–173) on top of this foundation.

## 🔗 Links

- 💻 Code: https://github.com/dharunvishnu2006-ctrl/autopilot-ml-x
- 🌐 Live App: https://autopilot-ml-x-v1-gprhnmfn2nhiemmsu8c6dp.streamlit.app/
- 📄 Design doc: [`docs/design.md`](docs/design.md)
- 📋 Decision records: [`docs/adr/`](docs/adr/)