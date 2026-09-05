import asyncio
import time
import pandas as pd
from src.ingest import ingest_all
from src.concurrency import ingest_all_threads, ingest_all_processes


def main():
    paths = [f"data/bench_{i}.csv" for i in range(8)]

    t0 = time.perf_counter()
    asyncio.run(ingest_all(paths))
    current_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    for p in paths:
        pd.read_csv(p)
    serial_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    asyncio.run(ingest_all_threads(paths))
    threads_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    asyncio.run(ingest_all_processes(paths))
    processes_time = time.perf_counter() - t0

    print(f"shipped 'async' version: {current_time:.2f}s")
    print(f"plain serial loop:       {serial_time:.2f}s")
    print(f"threads:                 {threads_time:.2f}s")
    print(f"processes:               {processes_time:.2f}s")
    print(f"ratio (async/serial): {current_time / serial_time:.2f}x")
    print(f"speedup (serial/threads): {serial_time / threads_time:.2f}x")
    print(f"speedup (serial/processes): {serial_time / processes_time:.2f}x")


if __name__ == "__main__":
    main()