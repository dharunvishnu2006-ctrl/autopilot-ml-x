import sqlite3


def get_conn():
    return sqlite3.connect("data/experiment_store.db")


def test_inner_join_returns_all_matched_runs():
    conn = get_conn()
    rows = conn.execute(
        "SELECT r.id FROM runs r "
        "JOIN experiments ex ON ex.id = r.experiment_id "
        "JOIN model_types mt ON mt.id = r.model_type_id"
    ).fetchall()
    assert len(rows) == 4


def test_left_join_anti_pattern_finds_unrun_experiments():
    conn = get_conn()
    rows = conn.execute(
        "SELECT ex.id FROM experiments ex "
        "LEFT JOIN runs r ON r.experiment_id = ex.id "
        "WHERE r.id IS NULL"
    ).fetchall()
    ids = {r[0] for r in rows}
    assert ids == {2}


def test_self_join_finds_same_model_pairs():
    conn = get_conn()
    rows = conn.execute(
        "SELECT a.id, b.id FROM runs a "
        "JOIN runs b ON a.model_type_id = b.model_type_id "
        "WHERE a.id < b.id"
    ).fetchall()
    pairs = set(rows)
    assert pairs == {(1, 3), (2, 4)}


def test_self_join_excludes_self_pairs():
    conn = get_conn()
    rows = conn.execute(
        "SELECT a.id, b.id FROM runs a "
        "JOIN runs b ON a.model_type_id = b.model_type_id "
        "WHERE a.id < b.id"
    ).fetchall()
    for a_id, b_id in rows:
        assert a_id != b_id
