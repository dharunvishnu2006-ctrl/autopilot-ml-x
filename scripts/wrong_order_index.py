import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
conn.execute(
    "CREATE INDEX idx_runs_time_exp " "ON runs(started_at DESC, experiment_id)"
)
conn.commit()
print("wrong-order index created")

query = (
    "SELECT r.id, r.started_at FROM runs r "
    "WHERE r.experiment_id = 1 "
    "ORDER BY r.started_at DESC LIMIT 10"
)
plan = conn.execute("EXPLAIN QUERY PLAN " + query).fetchall()
print("PLAN:", plan)
