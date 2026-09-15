import sys

sys.path.insert(0, "scripts")
from training_budget import (  # noqa: E402
    greedy_schedule,
    plan_budget,
    search_configs,
    match_renamed_columns,
)


def test_greedy_matches_optimal_when_it_can():
    experiments = [("A", 60, 10), ("B", 120, 15), ("C", 100, 12)]
    g_value, _ = greedy_schedule(experiments, 180)
    d_value, _ = plan_budget(experiments, 180)
    assert g_value == d_value


def test_greedy_loses_on_constructed_trap():
    trap = [("X", 1, 6), ("Y", 5, 7), ("Z", 5, 7)]
    g_value, _ = greedy_schedule(trap, 10)
    d_value, _ = plan_budget(trap, 10)
    assert g_value < d_value
    assert d_value == 14.0


def test_pruning_finds_same_valid_configs():
    depths = [1, 2, 3]
    lrs = [0.01, 0.1]
    valid_p, _ = search_configs(depths, lrs, 25, prune=True)
    valid_np, _ = search_configs(depths, lrs, 25, prune=False)
    assert set(valid_p) == set(valid_np)


def test_pruning_visits_fewer_or_equal_nodes():
    depths = [1, 2, 3]
    lrs = [0.01, 0.1]
    _, nodes_p = search_configs(depths, lrs, 25, prune=True)
    _, nodes_np = search_configs(depths, lrs, 25, prune=False)
    assert nodes_p <= nodes_np


def test_column_rename_matching():
    old = ["cust_id", "order_dt", "amt"]
    new = ["customer_id", "order_date", "amount", "region"]
    result = match_renamed_columns(old, new, threshold=4)
    assert result["cust_id"] == "customer_id"
    assert result["amt"] == "amount"


def test_column_rename_respects_threshold():
    old = ["zzz"]
    new = ["customer_id"]
    result = match_renamed_columns(old, new, threshold=2)
    assert "zzz" not in result
