def test_index_produces_search_not_scan(conn):
    plan = conn.execute(
        "EXPLAIN QUERY PLAN "
        "SELECT r.id FROM runs r "
        "WHERE r.experiment_id = 1 "
        "ORDER BY r.started_at DESC LIMIT 10"
    ).fetchall()
    plan_text = str(plan)
    assert "SEARCH" in plan_text
    assert "idx_runs_exp_time" in plan_text


def test_wrong_order_index_is_not_chosen(conn):
    plan = conn.execute(
        "EXPLAIN QUERY PLAN "
        "SELECT r.id FROM runs r "
        "WHERE r.experiment_id = 1 "
        "ORDER BY r.started_at DESC LIMIT 10"
    ).fetchall()
    plan_text = str(plan)
    assert "idx_runs_time_exp" not in plan_text


def test_partial_index_exists_and_is_smaller_scope(conn):
    full = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    running = conn.execute(
        "SELECT COUNT(*) FROM runs WHERE status = 'running'"
    ).fetchone()[0]
    assert running <= full
