import sqlite3

conn = sqlite3.connect("data/experiment_store.db")
conn.execute("DELETE FROM runs WHERE id IN (50, 51)")
conn.execute("DELETE FROM metrics WHERE run_id IN (50, 51)")
conn.commit()

try:
    conn.execute(
        "INSERT INTO runs VALUES "
        "(50,1,1,'done','trained','2026-02-01','2026-02-01','{}')"
    )
    conn.commit()
    raise RuntimeError("simulated crash before metrics insert")
    conn.execute("INSERT INTO metrics VALUES (50,50,'accuracy',0.99)")
    conn.commit()
except RuntimeError as e:
    print("crashed:", e)

check = conn.execute(
    "SELECT r.id, m.value FROM runs r "
    "LEFT JOIN metrics m ON m.run_id = r.id "
    "WHERE r.id = 50"
).fetchall()
print("orphan run:", check)

try:
    conn.execute("BEGIN")
    conn.execute(
        "INSERT INTO runs VALUES "
        "(51,1,1,'done','trained','2026-02-02','2026-02-02','{}')"
    )
    raise RuntimeError("simulated crash before metrics insert")
    conn.execute("INSERT INTO metrics VALUES (51,51,'accuracy',0.99)")
    conn.commit()
except RuntimeError as e:
    conn.rollback()
    print("crashed and rolled back:", e)

check2 = conn.execute("SELECT id FROM runs WHERE id = 51").fetchall()
print("run 51 exists:", check2)
