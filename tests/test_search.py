import sys

sys.path.insert(0, "scripts")
from search_runs import (  # noqa: E402
    linear_search,
    binary_search,
    search_on_answer,
    count_at_least,
    load_runs,
)

data = load_runs("data/seed_runs.csv")
sorted_data = sorted(data, key=lambda r: r[0])


def test_linear_finds_existing_run():
    result = linear_search(data, 4000)
    assert result[0] == 4000


def test_linear_missing_run_returns_none():
    result = linear_search(data, 999999)
    assert result is None


def test_binary_finds_existing_run():
    result = binary_search(sorted_data, 4000)
    assert result[0] == 4000


def test_binary_missing_run_returns_none():
    result = binary_search(sorted_data, 999999)
    assert result is None


def test_search_on_answer_meets_target():
    best = search_on_answer(data, 50)
    passing = count_at_least(data, best)
    assert passing >= 50
