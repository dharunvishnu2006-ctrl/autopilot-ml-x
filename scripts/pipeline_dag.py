from src.pipeline_dag import (
    Graph,
    bfs_reachable,
    has_cycle,
    topological_order,
)

pipe = Graph()
pipe.add_edge("load", "clean")
pipe.add_edge("clean", "features")
pipe.add_edge("features", "train")
print(pipe.adjacency)
print(pipe.neighbors("clean"))
print(pipe.neighbors("train"))

pipe2 = Graph()
pipe2.add_edge("load", "clean")
pipe2.add_edge("clean", "features")
pipe2.add_edge("features", "train")
pipe2.add_edge("clean", "validate")
print(bfs_reachable(pipe2, "clean"))

clean_pipe = Graph()
clean_pipe.add_edge("load", "clean")
clean_pipe.add_edge("clean", "features")
clean_pipe.add_edge("features", "train")
print(has_cycle(clean_pipe))

broken_pipe = Graph()
broken_pipe.add_edge("clean", "features")
broken_pipe.add_edge("features", "clean")
print(has_cycle(broken_pipe))

print(topological_order(pipe2))

try:
    topological_order(broken_pipe)
except ValueError as e:
    print(e)
