import pandas as pd
from collections import defaultdict


def read_chunks(path: str, chunk_size: int = 50_000):
    for chunk in pd.read_csv(path, chunksize=chunk_size):
        yield chunk


def read_rows(path: str):
    for chunk in read_chunks(path, chunk_size=1):
        yield chunk.iloc[0]

def profile_streaming(path: str, chunk_size: int = 50_000) -> dict:
    n = 0
    missing = defaultdict(int)
    total = defaultdict(float)
    lo = {}
    hi = {}

    for chunk in read_chunks(path, chunk_size):
        n += len(chunk)
        for col in chunk.columns:
            missing[col] += int(chunk[col].isna().sum())
            if pd.api.types.is_numeric_dtype(chunk[col]):
                total[col] += float(chunk[col].sum())
                col_min = float(chunk[col].min())
                col_max = float(chunk[col].max())
                lo[col] = min(lo.get(col, col_min), col_min)
                hi[col] = max(hi.get(col, col_max), col_max)

    means = {col: total[col] / (n - missing[col])
             for col in total if (n - missing[col]) > 0}

    return {"rows": n, "missing": dict(missing),
            "means": means, "min": lo, "max": hi}        