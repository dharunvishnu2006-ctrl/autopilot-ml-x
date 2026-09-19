import sqlite3

conn = sqlite3.connect(":memory:")  
conn.execute(
    "CREATE TABLE runs (id INTEGER, status TEXT)"
)  

query = open("scripts/funnel_query.sql").read()
result = conn.execute(query).fetchone()
print("empty table result:", result)