import sqlite3
import time

conn = sqlite3.connect("data/experiment_store.db")
query = open("scripts/measure_query.sql").read()
print(repr(query))

plan = conn.execute("EXPLAIN QUERY PLAN " + query).fetchall()
print("PLAN:", plan)

start = time.time()
for _ in range(50):
    conn.execute(query).fetchall()
elapsed = time.time() - start
print("50 runs took:", round(elapsed, 4), "s")
