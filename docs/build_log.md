# Build log

One entry per batch: what Claude Code built, what I changed, caught or
rejected, what I learned, and the time it took.

### Test-database fix (v2) - 21 Oct 2026

- **What Claude Code built:** scripts/build_test_db.py, the conftest
  fixtures (conn, engine) on a fresh database in tmp_path for every
  test, the guard test; 4 scripts moved under if __name__ == "__main__".
- **What I changed, caught or rejected:** found 3 September commits
  that existed only on the old laptop and rescued them onto GitHub with
  my real email; found the real cause of the "database is locked" bug
  (scripts/test_bad_insert.py collected by pytest) and fixed it by hand
  (testpaths, renames); caught that the lock was hiding dirty data and
  a test that only passed on leftover data; rejected leaving the old
  root conftest and Claude Code renaming files in data/; pinned
  SQLAlchemy, Alembic, greenlet and Mako after a fresh clone failed.
- **What I learned:** tests must never write to the real database;
  code at the top of a script runs on import; a fresh clone shows what
  my laptop was hiding.
- **Time:** about 5 hours (13:30-18:45).

### Home page polish (v2) - 22 Oct 2026

- **What Claude Code built:** src/brand.py, src/bootstrap.py (10,000
  synthetic runs from seed_runs.csv), src/home_queries.py,
  src/pipeline_dag.py, the new Home page, the sidebar, the light
  theme, 22 new tests; removed all 6 HTML blocks.
- **What I changed, caught or rejected:** kept Best accuracy 0.99 and
  the Datasets profiled card as the PDF has them; caught test junk in
  data/metadata.db (2 fake profiles), v1.0 showing 13% for 28/600 steps
  (fixed to 5%), and a test that only imported app.py. By hand: the
  Coming next lines to "- arrives in" like AAROGYA and Sentinel, and
  the Evolution test rewritten with AppTest and proved able to fail.
- **What I learned:** a test that cannot fail checks nothing; every
  number on the page has a chain: CSV, bootstrap, database, SQL, card.
- **Time:** about 5 hours (10:05-15:20).