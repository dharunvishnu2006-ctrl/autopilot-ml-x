# ADR 006: Migration Downgrade Data Loss

## Status
Accepted

## Context
I added a new `notes_v2` column to the `runs` table and inserted real data into it. Then I ran the migration downgrade, which dropped the column.

## Decision
Treat any downgrade that drops or changes data as destructive. Before running one, back up the affected data when possible. Prefer making old columns nullable and abandoned instead of dropping them.

## Consequences
Migrations will require more planning and backup steps before destructive downgrades. Some old columns may remain unused instead of being removed immediately, trading cleaner schemas for safer data recovery.

## Rejected Alternative
Running destructive downgrades without a backup, because dropped data cannot be recovered easily once the downgrade removes it.