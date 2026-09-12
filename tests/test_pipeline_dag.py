import sys 
sys.path.insert(0, "scripts")  
from pipeline_dag import (  # noqa: E402
    Graph, bfs_reachable, has_cycle, topological_order
)


def build_clean_pipeline():
    g = Graph()
    g.add_edge("load", "clean")
    g.add_edge("clean", "features")
    g.add_edge("features", "train")
    g.add_edge("clean", "validate")
    return g


def build_broken_pipeline():
    g = Graph()
    g.add_edge("clean", "features")
    g.add_edge("features", "clean")
    return g


def test_bfs_finds_all_downstream_stages():
    g = build_clean_pipeline()
    result = bfs_reachable(g, "clean")
    assert set(result) == {"clean", "features", "validate", "train"}


def test_bfs_excludes_upstream_stages():
    g = build_clean_pipeline()
    result = bfs_reachable(g, "clean")
    assert "load" not in result


def test_has_cycle_returns_none_for_valid_dag():
    g = build_clean_pipeline()
    assert has_cycle(g) is None


def test_has_cycle_names_the_actual_cycle():
    g = build_broken_pipeline()
    cycle = has_cycle(g)
    assert cycle is not None
    assert "clean" in cycle
    assert "features" in cycle


def test_topological_order_respects_dependencies():
    g = build_clean_pipeline()
    order = topological_order(g)
    assert order.index("load") < order.index("clean")
    assert order.index("clean") < order.index("features")
    assert order.index("features") < order.index("train")


def test_topological_order_raises_on_cycle():
    g = build_broken_pipeline()
    try:
        topological_order(g)
        assert False, "expected ValueError for cyclic graph"
    except ValueError as e:
        assert "clean" in str(e) or "features" in str(e)