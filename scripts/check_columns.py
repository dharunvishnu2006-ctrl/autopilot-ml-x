import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
cols = [row[1] for row in conn.execute("PRAGMA table_info(runs)")]
print(cols)
