## E8 — Parallel File Ingestion

### How

Tested multiple ways of loading files: serial, async, threads, and processes.
The benchmark showed **threads were the winner**, with `ThreadPoolExecutor` achieving about **1.46× speedup** over serial loading.

`ingest_all_threads()` was implemented in `src/concurrency.py` to load files concurrently using threads.

### Why

The original v1.0 approach used async ingestion, but the actual `pandas.read_*()` calls are blocking, so async did **not** provide the expected parallel speedup.

The benchmark exposed that mismatch: async was essentially the same speed as serial.
Threads were then tested and proved faster in the real workload.

So E8 was about **measuring what actually works instead of assuming concurrency makes things faster**.

### Where

The threaded implementation currently lives in:

`src/concurrency.py` → `ingest_all_threads()`

It is currently called by:

`scripts/benchmark_concurrency.py`

for benchmarking and comparison.

**Important:** `load_one()` has **not yet been changed to call `ingest_all_threads()`**. It still works the same way it did before E8.

The next integration step is to wire the threaded ingestion into the real pipeline so the production ingestion path can actually use the performance improvement. Until then, E8's threading implementation is **proven and measured, but not yet connected to the main pipeline**.


## E9 — NumPy Vectorized Statistics

### How

Added NumPy vectorization for mean, std, p50, p95, and IQR-based outlier counts. Measured a **146.5× speedup** over a Python loop, tested the NaN problem and chose a **drop-first policy**, and measured the memory difference between **float64 (8 MB)** and **float32 (4 MB)**.

### Why

Before E9, **NumPy was completely missing** from the project. For an ML platform, that was a real gap because NumPy provides the **core numerical foundation** that future ML models and calculations in v3+ will depend on.

### Where

Implemented in `column_stats()` as part of the project’s **data profiling/statistics path**.


## E10 — Grouped Profiling & Run Comparison

### How

Built `profile_by_group()` for segment-level statistics and `compare_runs()` using outer joins to detect dataset changes. Also caught the silent-drop problem with `how="inner"`.

### Why

To uncover **data-quality problems hidden by overall averages** and track meaningful changes between dataset runs.

### Where

Defined in the **data profiling/statistics code**, through `profile_by_group()` and `compare_runs()`. They are currently **proven and tested but not yet wired into the real pipeline or dashboard**; the tests are currently the only callers.


E11 — Dashboard Visualization & Integration
How
Added Matplotlib, Seaborn, and Plotly charts, fixed the plotting type bug, and made them work in both light and dark themes. Rewired uploads through `save_uploaded_file()` → `source_for()`.
Why
To fix two real dashboard problems: the hard-coded dark background made the dashboard hard to read in light mode, and directly using pd.read_csv(uploaded_file) bypassed source_for(), meaning dashboard uploads skipped the project's normal logging and instrumentation path.
Where
Used in `app.py`, where uploaded datasets are processed and visualized through the dashboard.

E13 — Quality Gates & Security
How

* Added pre-commit hooks for black, flake8, mypy, and bandit.
* Fixed the real issues those tools found: debug mode, type errors, lint errors, BOM encoding, and line-length conflicts.
* Retired the obsolete `test_invalid_file_rejected` test.
* Added `scripts/check.sh` to run the complete quality gate.
* Completed the first branch → PR → review → merge cycle.

Why
To catch security, typing, formatting, and code-quality problems automatically before they reach the main branch. This also fixed a real `debug=True` security vulnerability and removed a fake-passing test that could give false confidence.
Where
The checks run across the project through pre-commit and `scripts/check.sh`. The fixes covered `api.py`, configuration, tests, and other source files. The workflow is now enforced through the Git/PR process.
Result: 25 tests passing; flake8 21 → 0, mypy 7 → 0, bandit 62 findings → 0.


## E14 — LLM Summary Verification

### How

* Built `build_prompt()` with explicit grounding instructions.
* Built `verify()` to check every number against the source context.
* Built `summarize()` with fallback to the raw report on hallucination or API failure.
* Added a mocked LLM client so tests never touch the network.
* Added 7 verification/failure test cases.
* Documented the current limitation: column names are not verified.

### Why

To prevent an LLM-generated summary from introducing numbers that aren't actually in the dataset report. The verification step lets us reject hallucinated values and safely fall back to the original report.

### Where

The summarization and verification logic is used in the reporting/LLM layer. The LLM client is mocked in tests; this feature is currently proven without making real network calls.


## F1 — The Run Index

### How I built it
I first loaded the run data and built a linear search, then sorted the data and added binary search. After that I timed both approaches, built search-on-answer using `count_at_least()`, and tested all three approaches with pytest.

### Why it was needed
As run data grows to 100,000+ rows, scanning every row becomes slower. I measured both to confirm the real speed difference instead of assuming binary search would always be better.

### Where it's used in this project
In the dashboard, a user could search for a specific `run_id`, and the Run Index could use `binary_search` to find that run quickly. The Leaderboard could also use `search_on_answer` to find how many runs are above a certain accuracy.
