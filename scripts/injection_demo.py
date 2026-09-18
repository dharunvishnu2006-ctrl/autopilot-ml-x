import sqlite3

conn = sqlite3.connect("data/experiment_store.db")


def vulnerable_lookup(model_name):
    query = f"SELECT * FROM model_types WHERE name = '{model_name}'"
    return conn.execute(query).fetchall()


def safe_lookup(model_name):
    query = "SELECT * FROM model_types WHERE name = :name"
    return conn.execute(query, {"name": model_name}).fetchall()


print(vulnerable_lookup("rf"))

payload = "x' OR '1'='1"
print(vulnerable_lookup(payload))
print(safe_lookup(payload))
