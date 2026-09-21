import sqlite3


def get_conn():
    return sqlite3.connect("data/experiment_store.db")


def test_where_filters_done_runs():
    conn = get_conn()
    rows = conn.execute("SELECT id FROM runs WHERE status = 'done'").fetchall()
    ids = {r[0] for r in rows}
    assert ids == {1, 2, 4}


def test_order_by_desc_puts_newest_first():
    conn = get_conn()
    rows = conn.execute("SELECT id FROM runs ORDER BY started_at DESC").fetchall()
    ids = [r[0] for r in rows]
    assert ids == [4, 3, 2, 1]


def test_limit_returns_only_most_recent():
    conn = get_conn()
    rows = conn.execute(
        "SELECT id FROM runs ORDER BY started_at DESC LIMIT 1"
    ).fetchall()
    assert len(rows) == 1
    assert rows[0][0] == 4
