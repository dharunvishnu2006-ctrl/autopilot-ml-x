import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
triggers = list(conn.execute("SELECT name FROM sqlite_master WHERE type='trigger'"))
print(triggers)
