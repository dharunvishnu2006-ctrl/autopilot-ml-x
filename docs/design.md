# AutoPilot ML X — Design Document (v1.1)

## §1 — Problem

v1.0 shipped a working data-ingestion and profiling engine in three
days, but it used only 28 of the 80 roadmap steps in its range. An
audit of the shipped repository found six real defects, including a
concurrency claim in the README ("ingests files concurrently") that
was provably false. v1.1 closes the remaining 52 steps across 15
features (E1–E15), fixing all six defects and building the
foundations (NumPy, persistent history, engineering discipline) that
v2 through v6 depend on.

## §2 — Requirements (with measurements)

| Requirement | Measured Result |
|---|---|
| Bad files must not crash the pipeline | `IngestResult` typed failures; 3-file batch with 1 corrupt file survives (E1) |
| Every log line traceable to one run | `run_id` shared across START/FAIL/DONE lines, structured JSON (E2) |
| Profile history must survive a restart | SQLite, `runs`/`datasets`/`column_stats`, foreign keys enforced (E3) |
| Adding a file format = minimal change | One `DataSource` subclass + one registry entry (E5) |
| Profile files larger than RAM | Streaming: 8.9 MB peak vs 275.3 MB whole-file (31x less) on a 92MB file (E7) |
| Ingestion must be genuinely concurrent | Threads: 1.0s vs 1.5s shipped "async" — 1.46x real speedup (E8) |
| Statistics computed at ML-relevant speed | Vectorised mean: 0.91ms vs 133.92ms loop — 146.5x speedup (E9) |
| Segment-level data problems must be visible | Per-group missing rate (40% Chennai vs 10.5% overall) (E10) |
| Dashboard must work in any theme | Verified readable on both light and dark, programmatically composited (E11) |
| Dataset identity must be provable later | SHA256 fingerprint, 0.165s on a 92MB file, deterministic (E12) |
| Code quality enforced automatically | flake8 21→0, mypy 7→0, bandit 62→0 findings (E13) |
| LLM output must never show an invented number | `verify()` mechanically checks every number against source (E14) |

## §3 — Data Model

Three SQLite tables, linked by foreign keys, enforced via
`PRAGMA foreign_keys = ON` inside the `db()` context manager:

```
runs (id, run_id, started_at, source)
  └── datasets (id, run_id→runs.id, name, rows, cols, sha256)
        └── column_stats (id, dataset_id→datasets.id, name,
                           dtype, missing, unique_ct,
                           mean, p50, p95)
```

**NaN policy:** `column_stats()` (E9) explicitly drops NaN values
before computing statistics (`clean = values[~np.isnan(values)]`),
rather than relying on `np.nanmean()`-style functions throughout.
This is a deliberate, single, stated policy — not an accident —
chosen so the "drop" behavior is visible at one call site rather
than scattered implicitly across every statistic function.

## §4 — Concurrency Table

Measured on 8 × ~50MB CSV files (`data/bench_*.csv`), same machine,
same run:

| Approach | Time | vs. Serial |
|---|---|---|
| Shipped "async" (`asyncio.gather`) | ~1.43–1.55s | 1.04–1.06x (no real speedup) |
| Plain serial `for` loop | ~1.38–1.47s | baseline |
| **Threads** (`ThreadPoolExecutor`) | **~1.00s** | **~1.46x faster** |
| Processes (`ProcessPoolExecutor`) | ~1.41–1.42s | ~0.98–1.03x (no gain; Windows spawn/pickling overhead) |

cProfile confirmed the real hot spot is legitimate CSV parsing
(`pandas/io/parsers/readers.py:_read`), not a hidden inefficiency —
optimizing further would mean optimizing I/O itself, not application
code.

## §5 — Five Trade-offs

1. **One `DataSource` hierarchy over three copied if-elifs** — gave
   up a small abstraction layer, gained a single place that knows
   about formats (adding Parquet = one class + one registry line),
   and closed the gap where the dashboard bypassed instrumentation
   entirely (ADR 001).
2. **SQLite over memory-only profiling** — gave up some write I/O
   and storage overhead per run, gained history that survives a
   restart and enables the E10 change-report (ADR 002).
3. **Threads over asyncio/processes for ingestion** — measured, not
   assumed: asyncio was proven serial (1.04–1.06x ratio); processes
   lost to serial on this workload (0.98–1.03x) due to Windows
   spawn/pickling overhead; threads won because pandas' C parser
   releases the GIL (ADR 003).
4. **Streaming over reading the whole file** — gave up exact
   percentiles (median/p95 need the full distribution) and roughly
   1.7x more wall-clock time (6.48s vs 3.83s on a 2M-row file),
   gained ~31x less peak memory (8.9MB vs 275.3MB) — the trade-off
   that lets the profiler handle a file bigger than RAM.
5. **Verified LLM summaries over raw ones** — gave up some summaries
   entirely (any that fail verification fall back to the raw
   report), gained a hard guarantee that a shown summary never
   contains an invented number.

## §6 — Six Known Limits

1. **Exact percentiles need the whole column.** Streaming gives
   count, sum, mean, min, max in one pass; median and true
   percentiles cannot be computed incrementally without seeing every
   value (approximation techniques like t-digest exist but are out
   of scope for v1.1).
2. **The correlation heatmap caps at the top 15 columns by
   variance**, and with the current sample/synthetic data (which
   only has 2 numeric columns), it cannot demonstrate a genuinely
   large, sparse correlation matrix — this remains untested at
   scale.
3. **The LLM summary verifier checks numbers, not column names.** A
   summary could reference a fabricated column name and still pass
   verification, as long as it contains no invented numbers.
   Reliably detecting a fabricated column name via plain text
   matching is unreliable (English words overlap with real column
   names), so this is intentionally out of scope for now.
4. **SQLite is single-writer**; fine for one profiler instance, a
   real constraint if v2 introduces concurrent writers.
5. **Date detection is heuristic** (requires a separator character
   and a 90% parse hit-rate on a sample) and will miss unusual date
   formats or flag none at all on a column with too few non-null
   samples.
6. **`test_concurrent_beats_serial` depends on generated benchmark
   files** (`data/bench_*.csv`) that are gitignored — the test only
   passes on a machine where `make_benchmark_files.py` has already
   been run once.

## §7 — What v3 Will Need

- **NumPy foundations (E9)** — `column_stats()`'s vectorised
  mean/std/percentile/outlier-mask pattern is the same shape v3's
  model metrics will need.
- **The SHA256 fingerprint (E12)** — v3's model registry will record
  which dataset (by hash, not filename) trained which model.
- **The metadata store (E3)** — v3 needs a place to record which
  model was trained on which dataset snapshot; the `datasets` table
  already has a `sha256` column reserved for this.
- **The NaN-handling policy (E9, §3)** — v3's models will face the
  same "drop vs. impute" decision at a larger scale; the drop-first
  policy here is the starting precedent, not necessarily the final
  answer.