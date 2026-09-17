import sqlite3
import sys

conn = sqlite3.connect("data/experiment_store.db")
query = open(sys.argv[1]).read()
for row in conn.execute(query):
    print(row)
