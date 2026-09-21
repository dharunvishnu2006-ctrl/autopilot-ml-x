import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
query = "SELECT name FROM sqlite_master WHERE type='table'"
tables = [row[0] for row in conn.execute(query)]
print(tables)
