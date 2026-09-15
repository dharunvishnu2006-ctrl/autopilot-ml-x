import sys

sys.path.insert(0, "scripts")
from compute_path import (  # noqa: E402
    DSU,
    find_new_records,
    find_common,
    RollingAverage,
)


def test_dsu_union_find_after_chaining():
    nodes = [f"n{i}" for i in range(100)]
    dsu = DSU(nodes)
    for i in range(99):
        dsu.union(f"n{i}", f"n{i + 1}")
    assert dsu.find("n0") == dsu.find("n99")


def test_dsu_separate_groups_stay_separate():
    dsu = DSU(["a", "b", "c", "d"])
    dsu.union("a", "b")
    dsu.union("c", "d")
    assert dsu.find("a") == dsu.find("b")
    assert dsu.find("a") != dsu.find("c")


def test_find_new_records_correct_sequence():
    values = [0.7, 0.6, 0.9, 0.5, 0.95]
    assert find_new_records(values) == [0.7, 0.9, 0.95]


def test_find_new_records_all_increasing():
    values = [1, 2, 3, 4]
    assert find_new_records(values) == [1, 2, 3, 4]


def test_find_common_matches_set_intersection():
    a = [2, 4, 6, 8, 10]
    b = [4, 6, 9, 10]
    result = find_common(a, b)
    assert set(result) == set(a) & set(b)


def test_rolling_average_matches_manual_calc():
    roller = RollingAverage(3)
    assert roller.add(0.8) == 0.8
    assert roller.add(0.7) == (0.8 + 0.7) / 2
    assert roller.add(0.9) == (0.8 + 0.7 + 0.9) / 3
    result = roller.add(0.6)
    assert abs(result - (0.7 + 0.9 + 0.6) / 3) < 1e-9
