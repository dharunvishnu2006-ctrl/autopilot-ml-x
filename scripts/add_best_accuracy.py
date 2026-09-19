import sqlite3 

conn = sqlite3.connect("data/experiment_store.db")
conn.execute(
    "ALTER TABLE experiments ADD COLUMN best_accuracy REAL"
)
conn.commit()
print("column added")