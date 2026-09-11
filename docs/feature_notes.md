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


## F2 — The Leaderboard

### How I built it
I built bubble, insertion, merge, and quicksort from scratch and tested them. I then compared them with Python `sorted()`, using 300 items for bubble/insertion and 10,000 items for merge/quicksort/`sorted()`.

### Why it was needed
Without sorting, the Leaderboard can't efficiently arrange runs by accuracy. I built four algorithms to understand their differences instead of blindly using `sorted()`. Measuring them showed that Python's built-in `sorted()` was much faster than the hand built sorts. So in the real project I would use Python `sorted()` for the leaderboard and keep the four hand built sorts for learning and comparison.

### Where it's used in this project
The Leaderboard screen would use `sorted()` to arrange runs by accuracy and show the top 10. The four hand built sorts stay in the F2 learning/comparison code, not production.

## F3 — Top-K and the Job Queue

### How I built it
Built `top_k` with a heap, then `run_job_queue` with a priority queue and finally `counting_sort` for small range integers.

### Why it was needed
`top_k` avoids sorting the entire dataset just to find the best 10 runs, which matters as the data grows to millions of runs. `run_job_queue` exists because a critical model training job with a deadline should jump ahead of less urgent jobs that arrived earlier. `counting_sort` fits small range integer data such as epoch numbers or rank values, where the range is limited and known.

### Where it's used in this project
`top_k` would be used in the Leaderboard when only the top 10 runs are needed, instead of sorting all runs. `run_job_queue` sits in the background training process, letting urgent/critical training jobs run before normal jobs. `counting_sort` could be used for small-range integer data such as rank or epoch numbers when those values need to be sorted.

## F4 — The Pipeline Chain

### How I built it

I first built the LinkedList, then reused the node-chain idea for the UndoStack, Pipeline, and finally the FIFO Queue. While building the queue, I noticed LinkedList.append() had to walk from head to find the end every time, so I added a tail pointer to make new arrivals faster.

### Why it was needed

A linked list is not inherently better than a Python list for a simple fixed pipeline — a plain list of stage functions would work just as well; this was mainly practice building the chain structure. The UndoStack's `prev` pointer is also not strictly required — a Python list with `append()`/`pop()` handles undo perfectly well too. The Queue is different: FIFO order is a real requirement for processing runs in arrival order, though a plain Python list could also implement FIFO — the hand built linked list here is mainly an implementation/practice choice.

### Where it's used in this project

Currently these structures remain in the F4 learning implementation rather than having confirmed production call sites in AutoPilot ML X. The Queue models a real ingestion requirement (FIFO), but its hand built linked list implementation is not yet a required production component.

### Glossary

* **FIFO:** First item that enters is the first item that comes out.
* **LIFO:** Last item that enters is the first item that comes out.


## F5 — The Feature Cache

### How I built it
I built a HashTable with hashing, chaining, `put/get/delete`, then reused it for HashSet membership checks. Finally I built a Trie for character by character prefix searching. I also fixed a duplicate class bug that Python silently accepted but mypy caught.

### Why it was needed
F1's binary search organizes data around ordering; a hash table organizes data around identity. A feature cache cares about identity — "is this exact run configuration already here?" — so hashing is the more natural structure, giving average O(1) lookup instead of O(log n). HashSet wraps HashTable.put(key, True) so the code's intent is clear — `seen.add(key)` says "track membership" instead of exposing the raw implementation detail of a useless True value. A HashSet can only check one exact key in O(1); a pattern like `xgb_*` isn't a key, so answering it would mean scanning every key at O(n). A Trie stores shared prefixes, so it can jump straight to the `xgb_` branch and find all matches efficiently.

### Where it's used in this project
If someone runs xgb with max_depth=5, learning_rate=0.1 again, the HashTable cache would return the previously stored validation accuracy instead of retraining the model and recomputing that score. HashSet would be checked right before submitting a new training job to F3's job queue, to catch duplicates. The Trie powers the dashboard's model-search box, where a user types something like `xgb_` to quickly find all matching model names instead of scanning every one.

## F6 — The Experiment Tree

### How I built it
Built BST, then AVL, then Segment Tree. Hit a `RecursionError` with 1000 sorted BST values, proving the skew problem. Also fixed two method placement/indentation mistakes. Added segment tree range query and point update.

### Why it was needed
The plain BST hit height 500 and crashed at 1000 sorted inserts. AVL stayed at height 11 even with 2000 sorted inserts. At 1 million runs, repeated `max()` scans the requested range every time a user refreshes or changes a filter, so the cost keeps adding up. The Segment Tree reduces each range query to O(log n), making frequent dashboard queries scalable as data grows.

### Where it's used in this project
The Leaderboard would use `AVL.in_order()` to give runs sorted by accuracy. The Leaderboard screen's run range filter/slider — when a user selects Run 400 to Run 700 — would trigger the Segment Tree's range query to get the best accuracy in that window.