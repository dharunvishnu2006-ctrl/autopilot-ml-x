import sqlite3
import pytest


@pytest.fixture
def conn():
    connection = sqlite3.connect("data/experiment_store.db")
    yield connection
    connection.close()


def test_moving_average_grows_then_stabilizes(conn):
    rows = conn.execute(
        "SELECT r.id, AVG(m.value) OVER ("
        "ORDER BY r.started_at "
        "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW"
        ") FROM runs r "
        "JOIN metrics m ON m.run_id = r.id "
        "AND m.name = 'accuracy' ORDER BY r.started_at"
    ).fetchall()
    values = [r[1] for r in rows]
    assert abs(values[0] - 0.85) < 0.001
    assert abs(values[1] - 0.88) < 0.001
    assert abs(values[2] - 0.89) < 0.01


def test_check_constraint_rejects_negative_duration(conn):
    try:
        conn.execute(
            "INSERT INTO runs VALUES "
            "(99,1,1,'done','trained',"
            "'2026-01-10','2026-01-05','{}')"
        )
        assert False, "expected IntegrityError, insert succeeded"
    except sqlite3.IntegrityError:
        pass


def test_check_constraint_allows_null_finished_at(conn):
    conn.execute("BEGIN")
    conn.execute(
        "INSERT INTO runs VALUES "
        "(98,1,1,'running','trained',"
        "'2026-01-10',NULL,'{}')"
    )
    conn.rollback()


def test_coalesce_replaces_null_notes(conn):
    row = conn.execute("SELECT COALESCE(NULL, 'No notes')").fetchone()
    assert row[0] == "No notes"


def test_substr_extracts_prefix(conn):
    row = conn.execute("SELECT SUBSTR('xgboost', 1, 3)").fetchone()
    assert row[0] == "xgb"
