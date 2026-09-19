import sqlite3 

conn = sqlite3.connect("data/experiment_store.db")
conn.executescript(open("scripts/fts_setup.sql").read())
conn.commit()
print("FTS table created and populated")