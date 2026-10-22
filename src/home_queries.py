import sqlite3
from pathlib import Path

import src.store as store
from src.versions import load_versions

SQL_DIR = Path("scripts")


def _sql(name: str) -> str:
    # Read one repository SQL file
    return (SQL_DIR / name).read_text(encoding="utf-8")


def _one(conn, name: str, params=()) -> dict:
    # Run file, return first row
    cur = conn.execute(_sql(name), params)
    cols = [c[0] for c in cur.description]
    return dict(zip(cols, cur.fetchone()))


def _all(conn, name: str, params=()) -> list[dict]:
    # Run file, return every row
    cur = conn.execute(_sql(name), params)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def datasets_profiled(metadata_path: Path | None = None) -> int:
    # Count profiler datasets, 0 if missing
    path = Path(metadata_path or store.DB_PATH)
    if not path.exists():
        return 0
    uri = path.resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        return conn.execute("SELECT COUNT(*) FROM datasets").fetchone()[0]
    except sqlite3.OperationalError:
        return 0
    finally:
        conn.close()


def kpis(conn, metadata_path: Path | None = None) -> dict:
    # Collect the five Home numbers
    stats = _one(conn, "leaderboard_stats.sql")
    counts = _one(conn, "home_counts.sql")
    return {
        "experiments": counts["experiments"],
        "runs": stats["total_runs"],
        "best_accuracy": stats["best_accuracy"],
        "model_types": counts["model_types"],
        "datasets_profiled": datasets_profiled(metadata_path),
    }


def leaderboard(conn, top: int = 5) -> list[dict]:
    # Rank models by mean accuracy
    names = dict(conn.execute("SELECT id, name FROM model_types"))
    rows = _all(conn, "model_family_stats.sql")
    ranked = sorted(rows, key=lambda r: r["avg_accuracy"], reverse=True)
    return [
        {
            "model": names[r["model_type_id"]],
            "mean_accuracy": r["avg_accuracy"],
            "n": r["run_count"],
        }
        for r in ranked[:top]
    ]


def runs_per_day(conn) -> list[dict]:
    # Count runs for each day
    return _all(conn, "runs_per_day.sql")


def recent_runs(conn, n: int = 8) -> list[dict]:
    # Return newest runs with metrics
    return _all(conn, "recent_runs.sql", (n,))


def system_healthy(conn) -> bool:
    # Check versions and stored runs
    try:
        load_versions()
        runs = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    except (FileNotFoundError, ValueError, sqlite3.Error):
        return False
    return runs > 0
