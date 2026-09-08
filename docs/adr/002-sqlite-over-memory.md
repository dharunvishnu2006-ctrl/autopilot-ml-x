# ADR 002 — SQLite over Memory-Only Profiling

## Status
Accepted

## Context
Profiling produced results, but those results disappeared after
the process ended. That meant we could not later answer a key
question: did this dataset get worse compared with its previous
profile?

## Decision
We store profiling history in three SQLite tables: `runs`,
`datasets`, and `column_stats`, linked to their parent records
through foreign keys. All database access goes through the
`db()` context manager, which enables `PRAGMA foreign_keys = ON`
so invalid relationships are rejected.

## Consequences
Profiling history now survives process restarts and can be
compared across runs, enabling the change-report functionality
added later. The trade-off is additional SQLite write I/O and
some storage overhead for each profiling run.

## Rejected Alternative
We rejected memory-only profiling because previous results would
be lost when the process ended. This would prevent E10 from
comparing a new run against the previous profile — for example,
detecting that a Chennai dataset now has 40% missing values, or
that a previously present column has disappeared.