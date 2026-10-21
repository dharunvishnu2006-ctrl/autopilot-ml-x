# AutoPilot ML X - Test database fix
# Version: v2 (no new version). Built with Claude Code, before the
# home page polish. Written 21 October 2026.

## Problem
- The SQL tests open the real file data/experiment_store.db. Tests
  that write (test_sql_g7, g9, g11) commit rows that stay, so tests
  that run later read dirty data: 9 failures on 21 Oct 2026.
- data/*.db is git-ignored: a fresh clone has no database, so the
  SQL tests cannot run there.
- The home page polish will fill data/experiment_store.db with about
  10,000 synthetic runs; the SQL tests expect the 4-run teaching seed.

## Goal
Every test that needs the experiment store gets its own fresh
database in a temporary folder, built from files in the repository.
No test opens data/experiment_store.db.

## Tasks
1. One function, build_test_db(path): the tables from
   scripts/schema.sql, every later change the tests rely on (indexes,
   the best_accuracy column and its trigger, the FTS table,
   hyperparams, notes), then the 4-run seed of
   scripts/seed_sql_data.py. Reuse the existing .sql files. Where a
   step lives only in a script's top-level code, move it into a
   function that the script still calls, so the script works as
   before.
2. tests/conftest.py: a fixture that builds a fresh database in
   tmp_path for each test and yields a connection, closed after the
   test. Every SQL test uses it, including the SQLAlchemy engine in
   test_sql_g8.py (disposed after the test).
3. A guard test: fails if any file in tests/ opens
   data/experiment_store.db.
4. The full suite stays fast: about 30 seconds or less.

## Must not
- Change any assertion or expected value. If a test fails on the
  fresh seed, stop and show me the test and the values - I decide.
- Delete, skip or weaken a test. 159 earlier tests + the guard test.
- Touch app.py, src/, data/ or docs/; add a package. Only tests/
  and scripts/ change.

## Verification
- pytest -q twice in a row: same result, every test passes.
- data/experiment_store.db renamed away: pytest -q still passes.
- data/experiment_store.db has the same modified time before and
  after pytest -q.
- After the push, a fresh clone: pytest -q passes with no database.