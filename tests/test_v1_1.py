import asyncio
from src.ingest import load_one, ingest_all
from src.validation import DatasetSchema
from pathlib import Path
import json
import pandas as pd
import sqlite3
from src.store import db, init_db, save_profile
from src.sources import source_for, CSVSource, JSONSource, ExcelSource


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

def test_source_rejects_wrong_suffix():
    try:
        CSVSource("data/sample_orders.xlsx")
        assert False, "should have raised"
    except ValueError as e:
        assert "cannot read" in str(e)


def test_factory_dispatches_all_formats():
    assert isinstance(source_for("data/x.csv"), CSVSource)
    assert isinstance(source_for("data/x.json"), JSONSource)
    assert isinstance(source_for("data/x.xlsx"), ExcelSource)
    try:
        source_for("data/x.parquet")
        assert False, "should have raised"
    except ValueError as e:
        assert "Unsupported format" in str(e)    

def test_rollback_leaves_nothing():
    from src.store import db, init_db
    init_db()
    try:
        with db() as conn:
            conn.execute(
                "INSERT INTO runs "
                "(run_id, started_at, source) "
                "VALUES (?, ?, ?)",
                ("rollback_test", "2026-01-01", "x.csv"))
            raise ValueError("simulated failure")
    except ValueError:
        pass

    with db() as conn:
        row = conn.execute(
            "SELECT * FROM runs WHERE run_id = 'rollback_test'"
        ).fetchone()
    assert row is None        

def test_streaming_matches_full_read():
    from src.streaming import profile_streaming
    import pandas as pd

    df = pd.read_csv("data/sample_orders.csv")
    streamed = profile_streaming(
        "data/sample_orders.csv", chunk_size=1)

    assert streamed["rows"] == df.shape[0]
    assert streamed["missing"]["amount"] == int(
        df["amount"].isna().sum())
    expected_mean = float(df["amount"].mean())
    assert abs(streamed["means"]["amount"] - expected_mean) < 0.01    

def test_concurrent_beats_serial():
    import time
    from src.concurrency import ingest_all_threads
    from src.ingest import ingest_all

    paths = [f"data/bench_{i}.csv" for i in range(8)]

    t0 = time.perf_counter()
    asyncio.run(ingest_all(paths))
    shipped_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    asyncio.run(ingest_all_threads(paths))
    threads_time = time.perf_counter() - t0

    assert threads_time < shipped_time    