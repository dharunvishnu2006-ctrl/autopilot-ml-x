import numpy as np


def compare_mean_speed(n: int = 1_000_000):
    values = np.random.uniform(0, 1000, n)

    loop_total = 0.0
    for v in values:
        loop_total += v
    loop_mean = loop_total / n

    vectorized_mean = values.mean()

    return loop_mean, vectorized_mean

def column_stats(values: np.ndarray) -> dict:
    clean = values[~np.isnan(values)]
    if clean.size == 0:
        return {"n": 0}

    q1, q3 = np.percentile(clean, [25, 75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outlier_mask = (clean < lower) | (clean > upper)

    return {
        "n": int(clean.size),
        "mean": float(clean.mean()),
        "std": float(clean.std()),
        "p50": float(np.median(clean)),
        "p95": float(np.percentile(clean, 95)),
        "outliers": int(outlier_mask.sum()),
    }

def column_memory(values: np.ndarray) -> dict:
    original_mb = values.nbytes / 1_000_000
    downcast = values.astype(np.float32)
    downcast_mb = downcast.nbytes / 1_000_000
    return {
        "dtype": str(values.dtype),
        "original_mb": round(original_mb, 4),
        "downcast_mb": round(downcast_mb, 4),
    }