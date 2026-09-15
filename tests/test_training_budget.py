import sys

sys.path.insert(0, "scripts")
from training_budget import (  # noqa: E402
    to_mask,
    mask_to_names,
    fib_naive,
    fib_memo,
    best_subset_under_limit,
    edit_distance,
    plan_budget,
)


def test_bitmask_round_trip():
    m = to_mask(["a", "c"])
    assert set(mask_to_names(m)) == {"a", "c"}


def test_bitmask_union_and_intersection():
    m1 = to_mask(["a", "c"])
    m2 = to_mask(["c", "d"])
    assert set(mask_to_names(m1 | m2)) == {"a", "c", "d"}
    assert set(mask_to_names(m1 & m2)) == {"c"}


def test_fib_naive_and_memo_agree():
    for n in range(10):
        assert fib_naive(n) == fib_memo(n)


def test_memo_makes_far_fewer_calls():
    import training_budget as tb

    tb.call_count_naive = 0
    tb.call_count_memo = 0
    tb.fib_naive(15)
    tb.fib_memo(15)
    assert tb.call_count_memo < tb.call_count_naive


def test_best_subset_under_limit_correct():
    values = [3, 7, 2, 9]
    assert best_subset_under_limit(values, 2) == 16


def test_edit_distance_known_cases():
    assert edit_distance("cat", "cut") == 1
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("same", "same") == 0


def test_plan_budget_returns_value_and_plan():
    experiments = [("A", 60, 10), ("B", 120, 15), ("C", 100, 12)]
    value, plan = plan_budget(experiments, 180)
    assert value == 25.0
    assert set(plan) == {"A", "B"}


def test_plan_budget_respects_time_limit():
    experiments = [("A", 60, 10), ("B", 120, 15), ("C", 100, 12)]
    _, plan = plan_budget(experiments, 180)
    total_minutes = sum(cost for name, cost, val in experiments if name in plan)
    assert total_minutes <= 180
