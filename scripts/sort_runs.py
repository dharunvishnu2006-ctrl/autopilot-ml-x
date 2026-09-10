import csv
import time


def bubble_sort(values):
    arr = values.copy()
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(values):
    arr = values.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(values):
    if len(values) <= 1:
        return values.copy()
    mid = len(values) // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quicksort(values):
    if len(values) <= 1:
        return values.copy()
    pivot = values[-1]
    rest = values[:-1]
    smaller = [x for x in rest if x <= pivot]
    bigger = [x for x in rest if x > pivot]
    return quicksort(smaller) + [pivot] + quicksort(bigger)


sample = [5, 2, 8, 1]
print(bubble_sort(sample))
print(sample)
sample2 = [5, 2, 8, 1]
print(insertion_sort(sample2))

sample3 = [5, 2, 8, 1]
print(merge_sort(sample3))

sample4 = [5, 2, 8, 1]
print(quicksort(sample4))


def load_accuracies(path):
    values = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            if r[3] != "":
                values.append(float(r[3]))
    return values


accs = load_accuracies("data/seed_runs.csv")
small = accs[:300]
print(len(accs), len(small))


def time_it(fn, data):
    start = time.time()
    fn(data)
    return time.time() - start


bubble_t = time_it(bubble_sort, small)
insert_t = time_it(insertion_sort, small)
merge_t = time_it(merge_sort, accs)
quick_t = time_it(quicksort, accs)
builtin_t = time_it(sorted, accs)

print("bubble  (300):", round(bubble_t, 4), "s")
print("insert  (300):", round(insert_t, 4), "s")
print("merge (10000):", round(merge_t, 4), "s")
print("quick (10000):", round(quick_t, 4), "s")
print("sorted(10000):", round(builtin_t, 4), "s")
