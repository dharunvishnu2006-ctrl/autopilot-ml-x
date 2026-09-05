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
