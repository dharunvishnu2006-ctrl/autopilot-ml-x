# ADR 008: SQLite Workaround vs Blocking on PostgreSQL

## Status
Accepted

## Context
PostgreSQL setup was attempted, but port 5432 permission was denied and remained unresolved. I had to choose between blocking Block G entirely or continuing with SQLite.

## Decision
Continue G1 onward using SQLite where possible, while explicitly deferring PostgreSQL-only steps instead of blocking the entire project.

## Consequences
Steps 155-156, 169, 170, and step 171's restart proof remain deferred. SQLite required using FTS5 and JSON1 as substitutes for PostgreSQL-specific features.

## Rejected Alternative
Waiting for PostgreSQL would keep everything production-aligned and avoid substitutes, but it would block all other progress.