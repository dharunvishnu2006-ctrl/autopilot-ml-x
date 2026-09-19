import sqlite3  

def test_funnel_query_matches_real_data():
    conn = sqlite3.connect("data/experiment_store.db")
    row = conn.execute(open("scripts/funnel_query.sql").read()).fetchone()
    submitted, started, completed, pct = row
    assert submitted > 0
    assert completed <= started <= submitted


def test_funnel_query_handles_empty_table_safely():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE runs (id INTEGER, status TEXT)")
    row = conn.execute(open("scripts/funnel_query.sql").read()).fetchone()
    assert row == (0, 0, 0, None)