import sqlite3


def get_conn():
    return sqlite3.connect("data/experiment_store.db")


def test_count_star_vs_count_column_differ_with_nulls():
    conn = get_conn()
    row = conn.execute(
        "SELECT COUNT(*), COUNT(m.value) FROM runs r "
        "LEFT JOIN metrics m ON m.run_id = r.id "
        "AND m.name = 'accuracy'"
    ).fetchone()
    total, with_accuracy = row
    assert total == 4
    assert with_accuracy == 3
    assert total != with_accuracy


def test_avg_ignores_nulls_not_zeroes_them():
    conn = get_conn()
    row = conn.execute(
        "SELECT AVG(m.value) FROM runs r "
        "LEFT JOIN metrics m ON m.run_id = r.id "
        "AND m.name = 'accuracy'"
    ).fetchone()
    avg = row[0]
    assert abs(avg - 0.89) < 0.01


def test_having_filters_groups_correctly():
    conn = get_conn()
    rows = conn.execute(
        "SELECT r.model_type_id, COUNT(*) FROM runs r "
        "JOIN metrics m ON m.run_id = r.id "
        "AND m.name = 'accuracy' "
        "WHERE r.status = 'done' "
        "GROUP BY r.model_type_id "
        "HAVING COUNT(*) >= 1"
    ).fetchall()
    assert len(rows) == 2


def test_case_when_grades_correctly():
    conn = get_conn()
    rows = conn.execute(
        "SELECT r.id, "
        "CASE WHEN m.value > 0.95 THEN 'A' "
        "WHEN m.value > 0.90 THEN 'B' "
        "WHEN m.value > 0.80 THEN 'C' "
        "ELSE 'D' END "
        "FROM runs r JOIN metrics m ON m.run_id = r.id "
        "AND m.name = 'accuracy'"
    ).fetchall()
    grades = dict(rows)
    assert grades[1] == "C"
    assert grades[2] == "B"
