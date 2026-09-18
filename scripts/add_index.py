import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
conn.execute(
    "CREATE INDEX idx_runs_exp_time " "ON runs(experiment_id, started_at DESC)"
)
conn.commit()
print("index created")
