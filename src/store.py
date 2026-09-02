import sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime, timezone
import json

DB_PATH = Path("data") / "metadata.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    rows INTEGER NOT NULL,
    cols INTEGER NOT NULL,
    sha256 TEXT,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE TABLE IF NOT EXISTS column_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    dtype TEXT NOT NULL,
    missing INTEGER NOT NULL,
    unique_ct INTEGER,
    mean REAL, p50 REAL, p95 REAL,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id)
);

CREATE INDEX IF NOT EXISTS idx_column_stats_name
    ON column_stats(name);
"""

@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with db() as conn:
        conn.executescript(SCHEMA)

def discover_files(data_dir: str = "data") -> list[Path]:
    root = Path(data_dir)
    patterns = ["*.csv", "*.json", "*.xlsx"]
    found = []
    for pattern in patterns:
        found.extend(root.glob(pattern))
    return found        

def save_profile(run_id: str, source: str,
                  rows: int, cols: int,
                  column_stats: list[dict]) -> int:
    with db() as conn:
        cur = conn.execute(
            "INSERT INTO runs (run_id, started_at, source) "
            "VALUES (?, ?, ?)",
            (run_id, datetime.now(timezone.utc).isoformat(),
             source))
        run_pk = cur.lastrowid

        cur = conn.execute(
            "INSERT INTO datasets (run_id, name, rows, cols) "
            "VALUES (?, ?, ?, ?)",
            (run_pk, source, rows, cols))
        dataset_pk = cur.lastrowid

        for col in column_stats:
            conn.execute(
                "INSERT INTO column_stats "
                "(dataset_id, name, dtype, missing, "
                " unique_ct, mean, p50, p95) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (dataset_pk, col["name"], col["dtype"],
                 col["missing"], col.get("unique"),
                 col.get("mean"), col.get("p50"),
                 col.get("p95")))

        return dataset_pk    

def write_report(run_id: str, report: dict) -> Path:
    Path("reports").mkdir(exist_ok=True)
    path = Path("reports") / f"{run_id}.json"
    path.write_text(json.dumps(report, indent=2,
                                default=str))
    return path
