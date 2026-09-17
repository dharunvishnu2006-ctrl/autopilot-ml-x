import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
try:
    conn.execute(
        "INSERT INTO runs VALUES "
        "(5,1,1,'done','trained','2026-01-10','2026-01-05','{}')"
    )
    print("insert succeeded - constraint did NOT block it")
except sqlite3.IntegrityError as e:
    print("insert correctly rejected:", e)
