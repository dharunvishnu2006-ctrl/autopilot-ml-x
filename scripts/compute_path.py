import heapq
import time
from collections import deque


def dijkstra(graph, start):
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        cost, node = heapq.heappop(heap)
        if cost > dist[node]:
            continue
        for neighbor, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))
    return dist


pipeline_costs = {
    "load": [("clean", 2)],
    "clean": [("features", 3), ("validate", 1)],
    "features": [("train", 4)],
    "validate": [],
    "train": [],
}
print(dijkstra(pipeline_costs, "load"))

negative_graph = {
    "A": [("B", 4), ("C", 1)],
    "B": [("D", 1)],
    "C": [("B", -3)],
    "D": [],
}
print(dijkstra(negative_graph, "A"))


def dijkstra_naive(graph, start):
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    visited = set()
    heap = [(0, start)]

    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        for neighbor, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))
    return dist


trap_graph = {
    "A": [("B", 1), ("C", 2)],
    "B": [],
    "C": [("B", -3)],
}
print(dijkstra_naive(trap_graph, "A"))

real_trap = {
    "A": [("B", 1), ("C", 2)],
    "B": [("D", 1)],
    "C": [("B", -3)],
    "D": [],
}
print(dijkstra_naive(real_trap, "A"))


def bellman_ford(graph, start):
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    nodes = list(graph)
    edges = [(u, v, w) for u in graph for v, w in graph[u]]

    for _ in range(len(nodes) - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            raise ValueError("negative cycle detected")
    return dist


print(bellman_ford(real_trap, "A"))


def floyd_warshall(graph):
    nodes = list(graph)
    dist = {u: {v: float("inf") for v in nodes} for u in nodes}
    for u in nodes:
        dist[u][u] = 0
        for v, w in graph[u]:
            dist[u][v] = w

    for k in nodes:
        for i in nodes:
            for j in nodes:
                through_k = dist[i][k] + dist[k][j]
                if through_k < dist[i][j]:
                    dist[i][j] = through_k
    return dist


small_graph = {
    "A": [("B", 3)],
    "B": [("C", 2)],
    "C": [("A", 5)],
}
result = floyd_warshall(small_graph)
print(result["A"]["C"])
print(result["C"]["B"])


class DSU:
    def __init__(self, nodes):
        self.parent = {n: n for n in nodes}
        self.rank = {n: 0 for n in nodes}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        return True


def minimum_spanning_tree(nodes, edges):
    dsu = DSU(nodes)
    mst_edges = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
    return mst_edges


compute_nodes = ["n1", "n2", "n3", "n4"]
compute_edges = [
    ("n1", "n2", 4),
    ("n1", "n3", 1),
    ("n3", "n2", 2),
    ("n2", "n4", 5),
    ("n3", "n4", 8),
]
mst = minimum_spanning_tree(compute_nodes, compute_edges)
print(mst)
print(sum(w for _, _, w in mst))

big_nodes = [f"n{i}" for i in range(10000)]
dsu2 = DSU(big_nodes)
for i in range(len(big_nodes) - 1):
    dsu2.union(f"n{i}", f"n{i + 1}")

start_t = time.time()
for i in range(10000):
    dsu2.find(f"n{i}")
elapsed = time.time() - start_t
print("10000 finds after 10000 unions:", round(elapsed, 4), "s")


def find_new_records(values):
    stack = []
    records = []
    for v in values:
        while stack and stack[-1] <= v:
            stack.pop()
        if not stack:
            records.append(v)
        stack.append(v)
    return records


accuracies = [0.7, 0.6, 0.9, 0.5, 0.95]
print(find_new_records(accuracies))


def find_common(list_a, list_b):
    i, j = 0, 0
    common = []

    while i < len(list_a) and j < len(list_b):
        if list_a[i] == list_b[j]:
            common.append(list_a[i])
            i += 1
            j += 1
        elif list_a[i] < list_b[j]:
            i += 1
        else:
            j += 1
    return common


successful = [2, 4, 6, 8, 10]
flagged = [4, 6, 9, 10]
print(find_common(successful, flagged))


class RollingAverage:
    def __init__(self, size):
        self.size = size
        self.window = deque()
        self.total = 0

    def add(self, value):
        self.window.append(value)
        self.total += value
        if len(self.window) > self.size:
            removed = self.window.popleft()
            self.total -= removed
        return self.total / len(self.window)


roller = RollingAverage(3)
print(roller.add(0.8))
print(roller.add(0.7))
print(roller.add(0.9))
print(roller.add(0.6))
