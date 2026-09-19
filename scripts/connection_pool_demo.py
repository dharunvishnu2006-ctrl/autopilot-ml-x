from sqlalchemy import create_engine, text  
import concurrent.futures 
import time 

engine = create_engine(
    "sqlite:///data/experiment_store.db",
    pool_size=8,
    max_overflow=4,
    pool_pre_ping=True,
    pool_recycle=1800,
)


def slow_query(n):
    start = time.time() 
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        time.sleep(0.1)  
    return n, round(time.time() - start, 3)


with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
    results = list(ex.map(slow_query, range(20)))

waits = [r[1] for r in results]
print("fastest:", min(waits), "slowest:", max(waits))