import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
conn.execute("DELETE FROM metrics")
conn.execute("DELETE FROM runs")
conn.execute("DELETE FROM experiments")
conn.execute("DELETE FROM model_types")
conn.execute("DELETE FROM datasets")

conn.execute(
    "INSERT INTO datasets VALUES (1,'abc123','seed_runs',10003,6,'2026-01-01')"
)
conn.execute("INSERT INTO model_types VALUES (1,'rf','tree')")
conn.execute("INSERT INTO model_types VALUES (2,'xgb','tree')")
conn.execute("INSERT INTO experiments VALUES (1,'baseline',1,'2026-01-01','first try')")
conn.execute(
    "INSERT INTO runs VALUES " "(1,1,1,'done','trained','2026-01-01','2026-01-01','{}')"
)
conn.execute(
    "INSERT INTO runs VALUES " "(2,1,2,'done','trained','2026-01-02','2026-01-02','{}')"
)
conn.execute(
    "INSERT INTO runs VALUES " "(3,1,1,'failed','synthetic','2026-01-03',NULL,'{}')"
)
conn.execute("INSERT INTO metrics VALUES (1,1,'accuracy',0.85)")
conn.execute("INSERT INTO metrics VALUES (2,2,'accuracy',0.91)")
conn.execute("INSERT INTO metrics VALUES (3,1,'duration',120.5)")
conn.execute(
    "INSERT INTO runs VALUES " "(4,1,2,'done','trained','2026-01-04','2026-01-04','{}')"
)
conn.execute(
    "INSERT INTO experiments VALUES "
    "(2,'unused_experiment',1,'2026-01-05','never run')"
)

conn.commit()
print("seed data inserted")
