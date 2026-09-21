import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
conn.execute("PRAGMA journal_mode=WAL")
mode = conn.execute("PRAGMA journal_mode").fetchone()
print("journal mode:", mode)
conn.close()
