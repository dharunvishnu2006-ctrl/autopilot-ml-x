import sqlite3


def get_conn():
    return sqlite3.connect("data/experiment_store.db")


def test_rank_skips_after_tie_dense_rank_does_not():
    conn = get_conn()
    rows = conn.execute(
        "SELECT r.id, "
        "RANK() OVER (ORDER BY m.value DESC) AS rk, "
        "DENSE_RANK() OVER (ORDER BY m.value DESC) AS drk "
        "FROM runs r JOIN metrics m ON m.run_id = r.id "
        "AND m.name = 'accuracy' ORDER BY m.value DESC"
    ).fetchall()
    ranks = [r[1] for r in rows]
    dense_ranks = [r[2] for r in rows]
    assert ranks == [1, 1, 3]
    assert dense_ranks == [1, 1, 2]


def test_lag_is_positional_not_value_aware():
    conn = get_conn()
    rows = conn.execute(
        "SELECT r.id, "
        "LAG(m.value) OVER (ORDER BY r.started_at) AS prev "
        "FROM runs r LEFT JOIN metrics m ON m.run_id = r.id "
        "AND m.name = 'accuracy' ORDER BY r.started_at"
    ).fetchall()
    by_id = dict(rows)
    assert by_id[1] is None
    assert by_id[2] == 0.85
    assert by_id[3] == 0.91


def test_first_value_gives_same_baseline_to_every_row():
    conn = get_conn()
    rows = conn.execute(
        "SELECT r.id, "
        "FIRST_VALUE(m.value) OVER ("
        "PARTITION BY r.experiment_id ORDER BY r.started_at"
        ") AS baseline "
        "FROM runs r LEFT JOIN metrics m ON m.run_id = r.id "
        "AND m.name = 'accuracy'"
    ).fetchall()
    baselines = {r[1] for r in rows}
    assert baselines == {0.85}


def test_percent_rank_bounds_are_zero_and_one():
    conn = get_conn()
    rows = conn.execute(
        "SELECT PERCENT_RANK() OVER (ORDER BY m.value DESC) "
        "FROM runs r JOIN metrics m ON m.run_id = r.id "
        "AND m.name = 'accuracy'"
    ).fetchall()
    values = [r[0] for r in rows]
    assert min(values) == 0.0
    assert max(values) == 1.0
