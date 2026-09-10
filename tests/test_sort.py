import sys  # import path tools

sys.path.insert(0, "scripts")
from sort_runs import bubble_sort, insertion_sort, merge_sort, quicksort  # noqa: E402

UNSORTED = [5, 2, 8, 1, 9, 3]
EXPECTED = [1, 2, 3, 5, 8, 9]


def test_bubble_sort_correct():
    assert bubble_sort(UNSORTED) == EXPECTED


def test_insertion_sort_correct():
    assert insertion_sort(UNSORTED) == EXPECTED


def test_merge_sort_correct():
    assert merge_sort(UNSORTED) == EXPECTED


def test_quicksort_correct():
    assert quicksort(UNSORTED) == EXPECTED


def test_original_list_not_mutated():
    before = UNSORTED.copy()
    bubble_sort(UNSORTED)
    insertion_sort(UNSORTED)
    merge_sort(UNSORTED)
    quicksort(UNSORTED)
    assert UNSORTED == before
