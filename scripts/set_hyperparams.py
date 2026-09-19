import sqlite3 

conn = sqlite3.connect("data/experiment_store.db")
conn.execute(
    "UPDATE runs SET hyperparams = "
    "'{\"max_depth\": 5, \"learning_rate\": 0.1}' "
    "WHERE id = 1"
)
conn.commit()
print("hyperparams set")