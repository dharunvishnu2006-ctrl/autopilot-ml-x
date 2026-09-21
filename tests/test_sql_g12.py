def test_funnel_query_matches_real_data(conn):
    row = conn.execute(open("scripts/funnel_query.sql").read()).fetchone()
    submitted, started, completed, pct = row
    assert submitted > 0
    assert completed <= started <= submitted


def test_funnel_query_handles_empty_table_safely():
    import sqlite3

    mem_conn = sqlite3.connect(":memory:")
    mem_conn.execute("CREATE TABLE runs (id INTEGER, status TEXT)")
    row = mem_conn.execute(open("scripts/funnel_query.sql").read()).fetchone()
    assert row == (0, 0, 0, None)
