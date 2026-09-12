from collections import deque

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

pipe = Graph()
pipe.add_edge("load", "clean")
pipe.add_edge("clean", "features")
pipe.add_edge("features", "train")
print(pipe.adjacency)
print(pipe.neighbors("clean"))
print(pipe.neighbors("train"))    

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

pipe2 = Graph()
pipe2.add_edge("load", "clean")
pipe2.add_edge("clean", "features")
pipe2.add_edge("features", "train")
pipe2.add_edge("clean", "validate")
print(bfs_reachable(pipe2, "clean"))

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

clean_pipe = Graph()
clean_pipe.add_edge("load", "clean")
clean_pipe.add_edge("clean", "features")
clean_pipe.add_edge("features", "train")
print(has_cycle(clean_pipe))

broken_pipe = Graph()
broken_pipe.add_edge("clean", "features")
broken_pipe.add_edge("features", "clean")
print(has_cycle(broken_pipe))

def topological_order(graph):
    in_degree = {node: 0 for node in graph.adjacency}
    for node in graph.adjacency:
        for neighbor in graph.neighbors(node):
            in_degree[neighbor] += 1 

    queue = deque(
        sorted(n for n in in_degree if in_degree[n] == 0)
    )
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

print(topological_order(pipe2))

try:
    topological_order(broken_pipe)
except ValueError as e:
    print(e)