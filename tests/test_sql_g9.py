def test_transaction_prevents_orphan_run(conn):
    conn.execute("DELETE FROM runs WHERE id = 999")
    conn.commit()

    try:
        conn.execute("BEGIN")
        conn.execute(
            "INSERT INTO runs VALUES "
            "(999,1,1,'done','trained',"
            "'2026-03-01','2026-03-01','{}')"
        )
        raise RuntimeError("simulated crash")
        conn.execute("INSERT INTO metrics VALUES (999,999,'accuracy',0.9)")
        conn.commit()
    except RuntimeError:
        conn.rollback()

    row = conn.execute("SELECT id FROM runs WHERE id = 999").fetchone()
    assert row is None


def test_parameterized_query_blocks_injection_payload(conn):
    payload = "x' OR '1'='1"
    rows = conn.execute(
        "SELECT * FROM model_types WHERE name = :name",
        {"name": payload},
    ).fetchall()
    assert rows == []


def test_injection_payload_would_have_worked_unsafely(conn):
    payload = "x' OR '1'='1"
    query = f"SELECT * FROM model_types WHERE name = '{payload}'"
    rows = conn.execute(query).fetchall()
    assert len(rows) > 1
