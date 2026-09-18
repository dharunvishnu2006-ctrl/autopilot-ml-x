import sqlite3

conn = sqlite3.connect("data/experiment_store.db")

conn.execute("CREATE INDEX idx_full_status ON runs(status)")

conn.execute(
    "CREATE INDEX idx_partial_status ON runs(status) " "WHERE status = 'running'"
)
conn.commit()

full_count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
running_count = conn.execute(
    "SELECT COUNT(*) FROM runs WHERE status = 'running'"
).fetchone()[0]
print("full index covers:", full_count, "rows")
print("partial index covers:", running_count, "rows")
