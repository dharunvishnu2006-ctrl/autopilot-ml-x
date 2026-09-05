import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pandas as pd


async def ingest_all_threads(paths: list, max_workers: int = 8):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        tasks = [loop.run_in_executor(pool, pd.read_csv, p)
                 for p in paths]
        return await asyncio.gather(*tasks)


def _read_one(path):
    return pd.read_csv(path)


async def ingest_all_processes(paths: list, max_workers: int = 8):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        tasks = [loop.run_in_executor(pool, _read_one, p)
                 for p in paths]
        return await asyncio.gather(*tasks)