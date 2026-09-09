import csv
import time


def load_runs(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            r[0] = int(r[0])
            rows.append(r)
    return rows


def linear_search(rows, target_id):
    for row in rows:
        if row[0] == target_id:
            return row
    return None


data = load_runs("data/seed_runs.csv")
print(len(data))
found = linear_search(data, 4000)
print(found)

sorted_rows = sorted(data, key=lambda r: r[0])


def binary_search(rows, target_id):
    lo, hi = 0, len(rows) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_id = rows[mid][0]
        if mid_id == target_id:
            return rows[mid]
        elif mid_id < target_id:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


found2 = binary_search(sorted_rows, 4000)
print(found2)

N = 500
targets = list(range(N))

start = time.time()
for t in targets:
    linear_search(data, t)
linear_time = time.time() - start

start = time.time()
for t in targets:
    binary_search(sorted_rows, t)
binary_time = time.time() - start

print("linear:", round(linear_time, 4), "s")
print("binary:", round(binary_time, 4), "s")


def count_at_least(rows, threshold):
    count = 0
    for row in rows:
        if float(row[3] or 0) >= threshold:
            count += 1
    return count


def search_on_answer(rows, target_count):
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        c = count_at_least(rows, mid)
        if c >= target_count:
            lo = mid
        else:
            hi = mid
    return round(lo, 4)


best = search_on_answer(data, 50)
print(best)
print(count_at_least(data, best))
