import sqlite3
import random

random.seed(42)
conn = sqlite3.connect("data/experiment_store.db")
conn.execute("DELETE FROM runs WHERE id > 100")

rows = []
for i in range(101, 10101):
    exp_id = 1
    model_id = random.choice([1, 2])
    day = random.randint(1, 28)
    started = f"2026-02-{day:02d}"
    rows.append((i, exp_id, model_id, "done", "trained", started, started, "{}"))

conn.executemany("INSERT INTO runs VALUES (?,?,?,?,?,?,?,?)", rows)
conn.commit()
print("inserted", len(rows), "bulk runs")
