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
