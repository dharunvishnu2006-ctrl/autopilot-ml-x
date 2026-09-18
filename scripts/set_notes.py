import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
conn.execute("UPDATE runs SET notes_v2 = 'important note' WHERE id = 1")
conn.commit()
print(list(conn.execute("SELECT id, notes_v2 FROM runs WHERE id = 1")))
