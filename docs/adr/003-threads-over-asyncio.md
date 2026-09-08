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