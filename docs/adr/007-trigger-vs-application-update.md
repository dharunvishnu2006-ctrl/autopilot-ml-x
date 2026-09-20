# ADR 007: Trigger vs Application-Level Update

## Status
Accepted

## Context
I built a database trigger that automatically updates `experiments.best_accuracy` when a new metric has a better accuracy. The choice was whether to keep this logic in the database trigger or update `best_accuracy` from Python after each metric insert.

## Decision
Keep the database trigger, because it guarantees `best_accuracy` is updated whenever a new metric is inserted, regardless of which application code performs the insert.

## Consequences
The main cost is that the update logic is hidden in the database, so a Python developer may not find it while debugging or onboarding. Trigger behavior also needs separate database-level tests.

## Rejected Alternative
Python-side updates keep the logic visible and easier to debug and test, but every insert path must remember to update `best_accuracy` — a single missed call site would silently break the guarantee.