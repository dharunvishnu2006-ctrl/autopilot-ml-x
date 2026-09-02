import asyncio
from src.ingest import load_one, ingest_all
from src.validation import DatasetSchema
from pathlib import Path
import json
import pandas as pd
import sqlite3
from src.store import db, init_db, save_profile

def test_bad_file_returns_typed_failure():
    result = asyncio.run(load_one("data/does_not_exist.txt"))
    assert result.ok is False              
    assert "does_not_exist" in result.error  
    assert result.frame is None           

def test_run_survives_one_bad_file():
    paths = ["data/sample_orders.csv",
             "data/does_not_exist.txt",
             "data/sample_orders.csv"]
    results = asyncio.run(ingest_all(paths))
    oks = [r for r in results if r.ok]
    assert len(oks) == 2                
    assert len(results) == 3

def test_schema_rejects_bad_row():
    try:
        DatasetSchema(source="bad.csv", row_count=-1,
                      required_columns=["a"],
                      present_columns=["a"])
        assert False, "should have raised"
    except Exception as e:
        assert "bad.csv" in str(e)         

def test_no_print_in_src():
    for py_file in Path("src").glob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        assert "print(" not in text, (
            f"print() found in {py_file}")

def test_log_line_is_valid_json(capsys):
    from src.pipeline import pipeline

    @pipeline
    def sample():
        return 1

    sample()
    captured = capsys.readouterr()
    lines = [ln for ln in captured.out.strip().split("\n") if ln]
    for line in lines:
        parsed = json.loads(line)   
        assert "run_id" in parsed
        assert "ts" in parsed            

def test_date_column_detected():
    from src.cleaning import detect_date_columns

    df = pd.DataFrame({
        "signup_date": ["2024-01-15", "2024-02-03",
                         "2024-03-10", "2024-04-22"],
        "order_id": ["1001", "1002", "1003", "1004"],
    })
    detected = detect_date_columns(df)
    assert "signup_date" in detected  
    assert "order_id" not in detected            

def test_foreign_key_enforced():
    init_db()
    with db() as conn:
        try:
            conn.execute(
                "INSERT INTO datasets "
                "(run_id, name, rows, cols) "
                "VALUES (?, ?, ?, ?)",
                (999999, "ghost.csv", 1, 1))
            assert False, "should have raised"
        except sqlite3.IntegrityError:
            pass                          

def test_history_survives_reconnect():
    init_db()
    save_profile(run_id="hist1", source="persist.csv",
                 rows=5, cols=1,
                 column_stats=[{"name": "x", "dtype": "int64",
                                "missing": 0}])
    with db() as conn:
        row = conn.execute(
            "SELECT name FROM datasets "
            "WHERE name = 'persist.csv'").fetchone()
    assert row is not None
    assert row[0] == "persist.csv"


def test_index_is_used():
    init_db()
    with db() as conn:
        plan = conn.execute(
            "EXPLAIN QUERY PLAN "
            "SELECT * FROM column_stats WHERE name = 'x'"
        ).fetchall()
    plan_text = str(plan)
    assert "USING INDEX" in plan_text        

def test_mutable_default_not_shared():
    def collect(item, bucket=None):
        if bucket is None:
            bucket = []
        bucket.append(item)
        return bucket

    r1 = collect("a")
    r2 = collect("b")
    r3 = collect("c")
    assert r1 == ["a"]          
    assert r2 == ["b"]
    assert r3 == ["c"]        