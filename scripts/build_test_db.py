import sqlite3
from pathlib import Path

from scripts.add_best_accuracy import add_best_accuracy
from scripts.add_index import add_index
from scripts.seed_sql_data import seed
from scripts.set_hyperparams import set_hyperparams

SCRIPTS = Path(__file__).parent


def run_sql_file(conn, name):
    # Execute one repository .sql file
    conn.executescript((SCRIPTS / name).read_text(encoding="utf-8"))


def backfill_best_accuracy(conn):
    # Fill best_accuracy from seeded metrics
    conn.execute(
        "UPDATE experiments SET best_accuracy = ("
        "SELECT MAX(m.value) FROM metrics m "
        "JOIN runs r ON r.id = m.run_id "
        "WHERE r.experiment_id = experiments.id "
        "AND m.name = 'accuracy')"
    )


def build_test_db(path):
    # Build fresh seeded experiment store
    conn = sqlite3.connect(path)
    try:
        run_sql_file(conn, "schema.sql")
        seed(conn)
        add_best_accuracy(conn)
        add_index(conn)
        run_sql_file(conn, "create_trigger.sql")
        backfill_best_accuracy(conn)
        run_sql_file(conn, "fts_setup.sql")
        set_hyperparams(conn)
        conn.commit()
    finally:
        conn.close()
    return path
