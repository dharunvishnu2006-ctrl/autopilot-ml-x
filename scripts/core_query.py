from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/experiment_store.db")

query = text("SELECT id, status FROM runs WHERE status = :status")

with engine.connect() as conn:
    result = conn.execute(query, {"status": "done"})
    for row in result:
        print(row)
