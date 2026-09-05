import time
import numpy as np

values = np.random.uniform(0, 1000, 1_000_000)

t0 = time.perf_counter()
total = 0.0
for v in values:
    total += v
loop_mean = total / len(values)
loop_time = time.perf_counter() - t0

t0 = time.perf_counter()
vec_mean = values.mean()
vec_time = time.perf_counter() - t0

print(f"loop:       {loop_time*1000:.2f}ms, mean={loop_mean:.4f}")
print(f"vectorized: {vec_time*1000:.4f}ms, mean={vec_mean:.4f}")
print(f"speedup: {loop_time/vec_time:.1f}x")