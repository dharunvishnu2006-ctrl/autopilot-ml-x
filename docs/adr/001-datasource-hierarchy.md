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