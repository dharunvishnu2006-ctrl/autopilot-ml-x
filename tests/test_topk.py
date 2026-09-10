import sys

sys.path.insert(0, "scripts")
from topk_runs import top_k, run_job_queue, counting_sort  # noqa: E402


def test_top_k_returns_k_items():
    values = [5, 2, 8, 1, 9, 3, 7]
    result = top_k(values, 3)
    assert result == [9, 8, 7]


def test_top_k_handles_fewer_than_k():
    values = [5, 2]
    result = top_k(values, 5)
    assert result == [5, 2]


def test_job_queue_runs_most_urgent_first():
    jobs = [(3, "a"), (1, "b"), (2, "c")]
    order = run_job_queue(jobs)
    assert order == ["b", "c", "a"]


def test_counting_sort_matches_builtin():
    values = [3, 1, 2, 3, 1, 0]
    result = counting_sort(values, 3)
    assert result == sorted(values)
