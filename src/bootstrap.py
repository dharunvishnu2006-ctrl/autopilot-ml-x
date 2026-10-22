import csv
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from src.logging_setup import get_logger
from src.security import fingerprint

logger = get_logger("bootstrap")

DEFAULT_STORE = "data/experiment_store.db"
SCHEMA_FILE = Path("scripts/schema.sql")
SEED_CSV = Path("data/seed_runs.csv")
TIME_FMT = "%Y-%m-%d %H:%M:%S"
COUNTED = ["datasets", "model_types", "experiments", "runs", "metrics"]


def store_path() -> Path:
    # Read store path at call time
    return Path(os.environ.get("AUTOPILOT_STORE", DEFAULT_STORE))


def table_counts(conn) -> dict:
    # Count rows in every table
    counts = {}
    for table in COUNTED:
        sql = "SELECT COUNT(*) FROM " + table  # nosec B608
        counts[table] = conn.execute(sql).fetchone()[0]
    return counts


def _has_runs_table(conn) -> bool:
    # Check schema already exists
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='runs'"
    ).fetchone()
    return row is not None


def _read_seed(csv_path: Path) -> tuple[list[dict], int, int]:
    # Read CSV, drop duplicate run ids
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        n_cols = len(reader.fieldnames or [])
    seen: set[str] = set()
    unique = []
    for row in rows:
        if row["run_id"] not in seen:
            seen.add(row["run_id"])
            unique.append(row)
    return unique, len(rows), n_cols


def _finished_at(when: str, duration: str):
    # Add duration seconds to start
    if not duration:
        return None
    start = datetime.strptime(when, TIME_FMT)
    return (start + timedelta(seconds=float(duration))).strftime(TIME_FMT)


def _load_seed(conn, csv_path: Path) -> None:
    # Insert seed rows into tables
    rows, n_rows, n_cols = _read_seed(csv_path)
    first_seen = min(r["when"] for r in rows)
    conn.execute(
        "INSERT INTO datasets (id, sha256, name, rows, cols, first_seen) "
        "VALUES (1, ?, ?, ?, ?, ?)",
        (fingerprint(csv_path), csv_path.stem, n_rows, n_cols, first_seen),
    )

    models = sorted({r["model"] for r in rows})
    model_ids = {name: i for i, name in enumerate(models, start=1)}
    conn.executemany(
        "INSERT INTO model_types (id, name, family) VALUES (?, ?, NULL)",
        [(i, name) for name, i in model_ids.items()],
    )

    created: dict[int, str] = {}
    for r in rows:
        exp = int(r["exp_id"])
        created[exp] = min(created.get(exp, r["when"]), r["when"])
    conn.executemany(
        "INSERT INTO experiments (id, name, dataset_id, created_at, notes) "
        "VALUES (?, ?, 1, ?, 'synthetic')",
        [(e, f"exp_{e:03d}", t) for e, t in sorted(created.items())],
    )

    runs, metrics = [], []
    for r in rows:
        run_id = int(r["run_id"])
        status = "done" if r["accuracy"] else "failed"
        runs.append(
            (
                run_id,
                int(r["exp_id"]),
                model_ids[r["model"]],
                status,
                r["when"],
                _finished_at(r["when"], r["duration"]),
            )
        )
        if r["accuracy"]:
            metrics.append((run_id, "accuracy", float(r["accuracy"])))
        if r["duration"]:
            metrics.append((run_id, "duration", float(r["duration"])))
    conn.executemany(
        "INSERT INTO runs (id, experiment_id, model_type_id, status, "
        "source, started_at, finished_at, hyperparams) "
        "VALUES (?, ?, ?, ?, 'synthetic', ?, ?, '{}')",
        runs,
    )
    conn.executemany(
        "INSERT INTO metrics (run_id, name, value) VALUES (?, ?, ?)",
        metrics,
    )


def ensure_store(
    db_path: str | Path | None = None,
    schema: Path = SCHEMA_FILE,
    csv_path: Path = SEED_CSV,
) -> dict:
    # Build store once, return counts
    path = Path(db_path) if db_path else store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        with conn:
            if not _has_runs_table(conn):
                conn.executescript(schema.read_text(encoding="utf-8"))
            empty = conn.execute("SELECT COUNT(*) FROM runs").fetchone()
            if empty[0] == 0:
                _load_seed(conn, csv_path)
        counts = table_counts(conn)
    finally:
        conn.close()
    logger.info(f"experiment store ready: {counts}")
    return counts
