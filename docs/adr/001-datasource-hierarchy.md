# ADR 001 — DataSource Hierarchy

## Status
Accepted

## Context
The project had CSV/JSON/Excel file-dispatch logic duplicated
across three separate files. This duplication made the behavior
harder to keep consistent. More importantly, the dashboard had
its own copy of the dispatch logic and therefore bypassed the
`@pipeline` instrumentation used by the main path. That meant
dashboard-triggered processing could skip the project's logging
and timing information.

## Decision
We replaced the duplicated format-dispatch logic with a common
`DataSource` abstract base class and three concrete
implementations: `CSVSource`, `JSONSource`, and `ExcelSource`,
plus one factory function, `source_for()`, that picks the right
class based on file extension.

## Consequences
Adding a new format now needs only one new class + one registry
entry. The trade-off is a small abstraction layer instead of a
simple `if-elif` chain.

## Rejected Alternative
The old copied `if-elif` approach was rejected because the
dashboard used its own dispatch logic and bypassed `@pipeline`
instrumentation, causing its runs to miss the project's logging
and timing.

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

# ADR 003 — Threads over Asyncio/Processes for Ingestion

## Status
Accepted

## Context
The README claimed that file ingestion was concurrent, but the
shipped implementation used `asyncio.gather` around
`pd.read_csv()` calls that were actually blocking. Because
`pd.read_csv()` does not yield control back to the asyncio event
loop while it runs, the reads executed serially rather than
concurrently.

## Decision
We replaced the asyncio-based approach with threads using
`ThreadPoolExecutor`/`run_in_executor` to run file reads
concurrently. Threads work well here because pandas' C-based CSV
parser releases the GIL during parsing, allowing multiple file
reads to make progress in parallel despite Python's GIL.

## Consequences
Threads reduced the measured ingestion time to 1.0s, compared
with 1.5s for the shipped async version and 1.4s for plain
serial execution — about a 1.46x speedup.

## Rejected Alternatives
**Asyncio:** rejected because `pd.read_csv()` blocked the event
loop, making it effectively serial.

**Processes:** rejected because Windows spawn/pickling overhead
made them no faster than serial execution.