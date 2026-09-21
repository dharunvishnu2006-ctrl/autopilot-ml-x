# Debugging Log

## Entry 1: Intermittent "database is locked" on writes during full test suite

**Symptom:** Running `pytest -v` (159 tests) fails exactly 5 tests, always the
same ones, always with `sqlite3.OperationalError: database is locked` —
`test_sql_g7.py`'s two CHECK-constraint tests, `test_sql_g9.py`'s transaction
test, and `test_sql_g11.py`'s two trigger tests.

**What I tried:**
- Renamed a demo script that was accidentally being collected as a real test
  (fixed a real, separate bug).
- Converted all direct `sqlite3.connect()` calls in test files to a shared
  `conftest.py` fixture with guaranteed `connection.close()` (fixed real,
  separate unclosed-connection bugs in `test_sql_g2.py`, `test_sql_g3.py`,
  `test_sql_g4.py`, `test_sql_g5.py`, `test_sql_g6.py`, `test_sql_g9.py`,
  `test_sql_g10.py`, `test_sql_g11.py`, `test_sql_g12.py` — necessary
  fixes, but not sufficient to resolve the lock).
- Added `PRAGMA busy_timeout = 5000` to the fixture — no change.
- Switched the database to WAL journal mode — no change.
- Ran the failing tests in complete isolation, in a fresh terminal — all
  passed. Ran the full suite in that same fresh terminal — same 5 failures
  returned.
- Disposed SQLAlchemy engines explicitly in `test_sql_g8.py`
  (`engine.dispose()` after each test) — no change.

**Key finding:** every failing test performs a write (INSERT/DELETE/UPDATE);
every passing test, including ones in the same files, is read-only. This
points to something in the full-suite run sequence holding a write lock that
individual test runs don't trigger.

**Final status:** Unresolved after seven distinct fix attempts, each
addressing a genuine, real bug along the way (a demo script wrongly
collected as a test, unclosed connections in nine test files, an
outdated shipped-version assertion, and stale hardcoded expectations
in three files from evolving seed data). The five affected tests pass
reliably in isolation. The failure is perfectly reproducible on full-suite
runs on this specific machine only. Treating this as a known environment
quirk, comparable to the unresolved PostgreSQL port 5432 issue — both may
share a root cause in how this machine's OS/antivirus handles file locking.
Revisit with Process Monitor (Sysinternals) to see exactly what holds the
lock, or by testing on a completely different machine.