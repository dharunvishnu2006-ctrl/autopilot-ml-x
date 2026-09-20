# AutoPilot ML X

![version](https://img.shields.io/badge/version-v2-blue)
![tests](https://img.shields.io/badge/tests-159%20passing-brightgreen)
![python](https://img.shields.io/badge/python-3.14-blue)

> An ML experiment tracking platform, built roadmap-step by roadmap-step, with real measurements at every turn.

## What This Is

AutoPilot ML X is an ML experiment tracking project. v2 builds on v1.1 by adding Data Structures & Algorithms and SQL/Database engineering, with real tests and performance measurements.

## Results

- **18x faster index query**: 0.0523s → 0.0029s
- **Dijkstra bug**: naive Dijkstra returned 2, correct answer (via Bellman-Ford) was 0, with negative edge weights
- **AVL tree height**: 500 → 11, fixing the unbalanced tree problem
- **Memoization**: 21,891 → 39 function calls (naive vs memoized Fibonacci)
- **Greedy vs DP**: 13 vs DP's 14, proving the greedy choice was not optimal

## What Changed (v1.1 → v2)

| | v1.1 | v2 |
|---|---|---|
| Steps | 1–80 | 81–173 |
| Features | E1–E15 | F1–F12, G1–G12 |
| Tests | 44 | 159 |
| Focus | Ingestion & profiling engine | Data Structures & Algorithms, SQL & Databases |

## Known Limits

- **PostgreSQL setup is blocked on this Windows machine** — port 5432 permission denied, persists even as Administrator, with Windows Defender/AV checked and ruled out. Steps 155–156 remain deferred; SQLite serves G1 onward instead.
- **Step 169 (partitioning)** deferred — requires PostgreSQL's native partitioning.
- **Step 170 (replication) and step 171's `pool_pre_ping` restart proof** deferred for the same reason. Connection pool exhaustion was measured on SQLite as an illustration of the pooling mechanism, not a clean PostgreSQL-equivalent number.
- SQLite's FTS5 and JSON1 stand in for PostgreSQL's `tsvector` and `JSONB` throughout G11.

## What I Learned

DSA first and SQL second helped me connect concepts to real problems. The bugs, cross-machine work, and PostgreSQL blocker taught me to test honestly, document limits, and keep progressing.

## Architecture Decision Records

- [ADR 006](docs/adr/006-migration-downgrade-data-loss.md) — Destructive Migration Downgrades
- [ADR 007](docs/adr/007-trigger-vs-application-update.md) — Trigger vs Application-Level Update
- [ADR 008](docs/adr/008-sqlite-workaround-vs-blocking.md) — SQLite Workaround vs PostgreSQL Block