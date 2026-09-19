import sqlite3  


def test_rollup_grand_total_matches_sum_of_groups():
    conn = sqlite3.connect("data/experiment_store.db")
    rows = conn.execute(
        "SELECT model_type_id, COUNT(*) FROM runs "
        "GROUP BY model_type_id "
        "UNION ALL "
        "SELECT NULL, COUNT(*) FROM runs"
    ).fetchall()
    grand_total = [r[1] for r in rows if r[0] is None][0]
    group_sum = sum(r[1] for r in rows if r[0] is not None)
    assert grand_total == group_sum


def test_trigger_updates_best_accuracy_on_improvement():
    conn = sqlite3.connect("data/experiment_store.db")
    conn.execute("DELETE FROM metrics WHERE id = 200")
    conn.execute(
        "INSERT INTO metrics VALUES (200,1,'accuracy',0.97)"
    )
    conn.commit()
    row = conn.execute(
        "SELECT best_accuracy FROM experiments WHERE id = 1"
    ).fetchone()
    assert row[0] >= 0.97


def test_trigger_ignores_worse_accuracy():
    conn = sqlite3.connect("data/experiment_store.db")
    before = conn.execute(
        "SELECT best_accuracy FROM experiments WHERE id = 1"
    ).fetchone()[0]
    conn.execute("DELETE FROM metrics WHERE id = 201")
    conn.execute(
        "INSERT INTO metrics VALUES (201,1,'accuracy',0.01)"
    )
    conn.commit()
    after = conn.execute(
        "SELECT best_accuracy FROM experiments WHERE id = 1"
    ).fetchone()[0]
    assert after == before  


def test_fts_search_finds_matching_notes():
    conn = sqlite3.connect("data/experiment_store.db")
    rows = conn.execute(
        "SELECT rowid FROM experiments_fts "
        "WHERE experiments_fts MATCH 'first'"
    ).fetchall()
    assert rows == [(1,)]


def test_json_extract_reads_hyperparams():
    conn = sqlite3.connect("data/experiment_store.db")
    row = conn.execute(
        "SELECT json_extract(hyperparams, '$.max_depth') "
        "FROM runs WHERE id = 1"
    ).fetchone()
    assert row[0] == 5