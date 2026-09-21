import sqlite3


def get_conn():
    return sqlite3.connect("data/experiment_store.db")


def test_rank_derived_table_finds_best_run():
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM ("
        "  SELECT r.id, r.experiment_id, m.value, "
        "  RANK() OVER (PARTITION BY r.experiment_id "
        "  ORDER BY m.value DESC) AS rk "
        "  FROM runs r JOIN metrics m ON m.run_id = r.id "
        "  AND m.name = 'accuracy'"
        ") t WHERE t.rk = 1"
    ).fetchall()
    assert len(rows) == 2  # two runs tie for the best accuracy
    values = {row[2] for row in rows}
    assert values == {0.91}


def test_cte_matches_derived_table_result():
    conn = get_conn()
    row = conn.execute(
        "WITH ranked AS ("
        "  SELECT r.id, r.experiment_id, m.value, "
        "  RANK() OVER (PARTITION BY r.experiment_id "
        "  ORDER BY m.value DESC) AS rk "
        "  FROM runs r JOIN metrics m ON m.run_id = r.id "
        "  AND m.name = 'accuracy'"
        "), best AS (SELECT * FROM ranked WHERE rk = 1) "
        "SELECT best.value FROM best LIMIT 1"
    ).fetchone()
    assert row[0] == 0.91


def test_recursive_calendar_has_no_gaps():
    conn = get_conn()
    rows = conn.execute(
        "WITH RECURSIVE days(d) AS ("
        "  SELECT DATE('2026-01-01') "
        "  UNION ALL "
        "  SELECT date(d, '+1 day') FROM days "
        "  WHERE d < DATE('2026-01-10')"
        ") "
        "SELECT days.d, COUNT(r.id) FROM days "
        "LEFT JOIN runs r ON DATE(r.started_at) = days.d "
        "GROUP BY days.d ORDER BY days.d"
    ).fetchall()
    assert len(rows) == 10
    zero_run_days = [r for r in rows if r[1] == 0]
    assert len(zero_run_days) == 6
