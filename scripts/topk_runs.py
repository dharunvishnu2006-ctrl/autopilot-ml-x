import heapq
import csv


def load_accuracies(path):
    values = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            if r[3] != "":
                values.append(float(r[3]))
    return values


def top_k(values, k):
    heap = []
    for v in values:
        if len(heap) < k:
            heapq.heappush(heap, v)
        elif v > heap[0]:
            heapq.heapreplace(heap, v)
    return sorted(heap, reverse=True)


accs = load_accuracies("data/seed_runs.csv")
best10 = top_k(accs, 10)
print(best10)


def run_job_queue(jobs):
    heap = []
    for priority, name in jobs:
        heapq.heappush(heap, (priority, name))

    order = []
    while heap:
        priority, name = heapq.heappop(heap)
        order.append(name)
    return order


pending = [(3, "job_a"), (1, "job_b"), (2, "job_c")]
print(run_job_queue(pending))


def counting_sort(values, max_val):
    counts = [0] * (max_val + 1)
    for v in values:
        counts[v] += 1

    result = []
    for val in range(max_val + 1):
        result.extend([val] * counts[val])
    return result


sample5 = [3, 1, 2, 3, 1]
print(counting_sort(sample5, 3))
