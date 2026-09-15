FEATURES = ["a", "b", "c", "d"]


def to_mask(selected):
    mask = 0
    for name in selected:
        bit = FEATURES.index(name)
        mask |= 1 << bit
    return mask


def mask_to_names(mask):
    names = []
    for bit, name in enumerate(FEATURES):
        if mask & (1 << bit):
            names.append(name)
    return names


m = to_mask(["a", "c"])
print(m)
print(mask_to_names(m))

m2 = m | to_mask(["b"])
print(m2)
print(mask_to_names(m2))

m3 = m & to_mask(["c", "d"])
print(mask_to_names(m3))

call_count_naive = 0


def fib_naive(n):
    global call_count_naive
    call_count_naive += 1
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


call_count_memo = 0


def fib_memo(n, cache=None):
    global call_count_memo
    if cache is None:
        cache = {}
    call_count_memo += 1
    if n <= 1:
        return n
    if n in cache:
        return cache[n]
    result = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    cache[n] = result
    return result


print(fib_naive(20))
print("naive calls:", call_count_naive)

print(fib_memo(20))
print("memo calls:", call_count_memo)


def best_subset_under_limit(values, limit):
    n = len(values)
    dp = [[0] * (limit + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        val = values[i - 1]
        for k in range(limit + 1):
            dp[i][k] = dp[i - 1][k]
            if k >= 1:
                with_it = dp[i - 1][k - 1] + val
                dp[i][k] = max(dp[i][k], with_it)
    return dp[n][limit]


feature_values = [3, 7, 2, 9]
print(best_subset_under_limit(feature_values, 2))


def edit_distance(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                delete = dp[i - 1][j] + 1
                insert = dp[i][j - 1] + 1
                replace = dp[i - 1][j - 1] + 1
                dp[i][j] = min(delete, insert, replace)
    return dp[n][m]


print(edit_distance("cat", "cut"))
print(edit_distance("kitten", "sitting"))


def plan_budget(experiments, budget_minutes):
    n = len(experiments)
    B = budget_minutes
    dp = [[0.0] * (B + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, cost, val = experiments[i - 1]
        for b in range(B + 1):
            dp[i][b] = dp[i - 1][b]
            if cost <= b:
                with_it = dp[i - 1][b - cost] + val
                dp[i][b] = max(dp[i][b], with_it)

    chosen = []
    b = B
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name, cost, val = experiments[i - 1]
            chosen.append(name)
            b -= cost
    chosen.reverse()
    return dp[n][B], chosen


experiments = [("A", 60, 10), ("B", 120, 15), ("C", 100, 12)]
value, plan = plan_budget(experiments, 180)
print(value)
print(plan)


def greedy_schedule(experiments, budget_minutes):
    ranked = sorted(experiments, key=lambda e: e[2] / e[1], reverse=True)
    remaining = budget_minutes
    chosen = []
    total_value = 0

    for name, cost, val in ranked:
        if cost <= remaining:
            chosen.append(name)
            remaining -= cost
            total_value += val
    return total_value, chosen


trap_experiments = [
    ("X", 1, 6),
    ("Y", 5, 7),
    ("Z", 5, 7),
]
g_value, g_plan = greedy_schedule(trap_experiments, 10)
d_value, d_plan = plan_budget(trap_experiments, 10)
print("greedy:", g_value, g_plan)
print("optimal:", d_value, d_plan)


def search_configs(depths, lrs, budget, prune=True):
    valid = []
    nodes_visited = [0]

    def backtrack(chosen, cost):
        nodes_visited[0] += 1
        if prune and cost > budget:
            return
        if len(chosen) == 2:
            if cost <= budget:
                valid.append(tuple(chosen))
            return
        if len(chosen) == 0:
            for d in depths:
                backtrack(chosen + [d], cost + d * 10)
        else:
            for lr in lrs:
                backtrack(chosen + [lr], cost)

    backtrack([], 0)
    return valid, nodes_visited[0]


depths = [1, 2, 3]
lrs = [0.01, 0.1]

valid_p, nodes_p = search_configs(depths, lrs, 25, prune=True)
valid_np, nodes_np = search_configs(depths, lrs, 25, prune=False)

print(valid_p)
print("pruned nodes:", nodes_p)
print(valid_np)
print("unpruned nodes:", nodes_np)


def match_renamed_columns(old_cols, new_cols, threshold):
    matches = {}
    for old in old_cols:
        best_match = None
        best_dist = threshold + 1
        for new in new_cols:
            d = edit_distance(old.lower(), new.lower())
            if d < best_dist:
                best_dist = d
                best_match = new
        if best_dist <= threshold:
            matches[old] = best_match
    return matches


old_columns = ["cust_id", "order_dt", "amt"]
new_columns = ["customer_id", "order_date", "amount", "region"]
print(match_renamed_columns(old_columns, new_columns, threshold=4))
