import sys  
sys.path.insert(0, "scripts")  
from compute_path import (  # noqa: E402
    dijkstra, dijkstra_naive, bellman_ford,
    floyd_warshall, minimum_spanning_tree
)


def test_dijkstra_correct_on_positive_weights():
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2)],
        "C": [],
    }
    result = dijkstra(graph, "A")
    assert result["C"] == 3  # via A->B->C


def test_dijkstra_wrong_on_negative():
    graph = {
        "A": [("B", 1), ("C", 2)],
        "B": [("D", 1)],
        "C": [("B", -3)],
        "D": [],
    }
    wrong = dijkstra_naive(graph, "A")
    correct = bellman_ford(graph, "A")
    assert wrong["D"] != correct["D"]  
    assert correct["D"] == 0  


def test_bellman_ford_matches_dijkstra_when_positive():
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2)],
        "C": [],
    }
    dj = dijkstra(graph, "A")
    bf = bellman_ford(graph, "A")
    assert dj == bf 

def test_floyd_warshall_matches_dijkstra():
    graph = {
        "A": [("B", 3)],
        "B": [("C", 2)],
        "C": [("A", 5)],
    }
    fw = floyd_warshall(graph)
    for start in graph:
        dj = dijkstra(graph, start)
        for end in graph:
            assert fw[start][end] == dj[end]


def test_mst_connects_all_nodes_at_minimum_cost():
    nodes = ["n1", "n2", "n3", "n4"]
    edges = [
        ("n1", "n2", 4), ("n1", "n3", 1),
        ("n3", "n2", 2), ("n2", "n4", 5),
        ("n3", "n4", 8),
    ]
    mst = minimum_spanning_tree(nodes, edges)
    assert len(mst) == len(nodes) - 1  
    assert sum(w for _, _, w in mst) == 8