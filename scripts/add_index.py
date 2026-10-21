import sqlite3


def add_index(conn):
    # Create experiment-then-time runs index
    conn.execute(
        "CREATE INDEX idx_runs_exp_time " "ON runs(experiment_id, started_at DESC)"
    )


if __name__ == "__main__":
    conn = sqlite3.connect("data/experiment_store.db")
    add_index(conn)
    conn.commit()
    print("index created")
