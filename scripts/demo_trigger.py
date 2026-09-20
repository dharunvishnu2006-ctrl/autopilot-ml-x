import sqlite3  

conn = sqlite3.connect("data/experiment_store.db")
conn.execute("DELETE FROM metrics WHERE id IN (100, 101)")
conn.commit()

conn.execute(
    "INSERT INTO metrics VALUES (100,1,'accuracy',0.99)"
)
conn.commit()

result = conn.execute(
    "SELECT best_accuracy FROM experiments WHERE id = 1"
).fetchone()
print("best_accuracy after insert:", result)

conn.execute(
    "INSERT INTO metrics VALUES (101,1,'accuracy',0.5)"
)
conn.commit()

result2 = conn.execute(
    "SELECT best_accuracy FROM experiments WHERE id = 1"
).fetchone()
print("best_accuracy after worse insert:", result2)