from collections import deque

DOT_SIZE = "4,2"


class Graph:
    def __init__(self):
        self.adjacency = {}

    def add_node(self, name):
        if name not in self.adjacency:
            self.adjacency[name] = []

    def add_edge(self, source, target):
        self.add_node(source)
        self.add_node(target)
        self.adjacency[source].append(target)

    def neighbors(self, name):
        return self.adjacency.get(name, [])


def bfs_reachable(graph, start):
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def has_cycle(graph):
    WHITE, GREY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph.adjacency}

    def visit(node, path):
        color[node] = GREY
        path.append(node)
        for neighbor in graph.neighbors(node):
            if color[neighbor] == GREY:
                cycle_start = path.index(neighbor)
                return path[cycle_start:] + [neighbor]
            if color[neighbor] == WHITE:
                result = visit(neighbor, path)
                if result:
                    return result
        color[node] = BLACK
        path.pop()
        return None

    for node in graph.adjacency:
        if color[node] == WHITE:
            result = visit(node, [])
            if result:
                return result
    return None


def topological_order(graph):
    in_degree = {node: 0 for node in graph.adjacency}
    for node in graph.adjacency:
        for neighbor in graph.neighbors(node):
            in_degree[neighbor] += 1

    queue = deque(sorted(n for n in in_degree if in_degree[n] == 0))
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.neighbors(node):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(graph.adjacency):
        stuck = sorted(set(graph.adjacency) - set(order))
        raise ValueError(f"Cycle involving: {stuck}")
    return order


def home_pipeline():
    # Build the v2 pipeline stages
    g = Graph()
    g.add_edge("load", "clean")
    g.add_edge("clean", "features")
    g.add_edge("features", "train")
    g.add_edge("clean", "validate")
    return g


def to_dot(graph):
    # Render graph as DOT text
    lines = [
        "digraph pipeline {",
        f'  graph [rankdir=LR, size="{DOT_SIZE}"];',
        "  node [shape=box, style=rounded];",
    ]
    for node in topological_order(graph):
        for neighbor in graph.neighbors(node):
            lines.append(f'  "{node}" -> "{neighbor}";')
    lines.append("}")
    return "\n".join(lines)
