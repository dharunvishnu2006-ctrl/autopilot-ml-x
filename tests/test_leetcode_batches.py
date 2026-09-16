import sys

sys.path.insert(0, "scripts")
from leetcode_batches import (  # noqa: E402
    two_sum,
    contains_duplicate,
    intersection,
    valid_parentheses,
    climbing_stairs,
    max_subarray,
    move_zeroes,
    ListNode,
    reverse_linked_list,
    has_cycle,
    longest_substring_no_repeat,
    coin_change,
    num_islands,
    merge_intervals,
)


def test_two_sum_finds_pair():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]


def test_contains_duplicate():
    assert contains_duplicate([1, 2, 3, 1]) is True
    assert contains_duplicate([1, 2, 3]) is False


def test_intersection_finds_common():
    assert set(intersection([1, 2, 3], [2, 3, 4])) == {2, 3}


def test_valid_parentheses():
    assert valid_parentheses("([)]") is False
    assert valid_parentheses("([{}])") is True


def test_climbing_stairs():
    assert climbing_stairs(5) == 8


def test_max_subarray():
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6


def test_move_zeroes():
    assert move_zeroes([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]


def test_reverse_linked_list():
    n1 = ListNode(1)
    n2 = ListNode(2)
    n3 = ListNode(3)
    n1.next = n2
    n2.next = n3
    new_head = reverse_linked_list(n1)
    result = []
    node = new_head
    while node:
        result.append(node.val)
        node = node.next
    assert result == [3, 2, 1]


def test_has_cycle_detects_real_cycle():
    c1 = ListNode(1)
    c2 = ListNode(2)
    c3 = ListNode(3)
    c1.next = c2
    c2.next = c3
    c3.next = c1
    assert has_cycle(c1) is True


def test_has_cycle_no_cycle():
    c4 = ListNode(1)
    c5 = ListNode(2)
    c4.next = c5
    assert has_cycle(c4) is False


def test_longest_substring_no_repeat():
    assert longest_substring_no_repeat("abcabcbb") == 3
    assert longest_substring_no_repeat("bbbbb") == 1
    assert longest_substring_no_repeat("pwwkew") == 3


def test_coin_change():
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1


def test_num_islands():
    grid = [
        ["1", "1", "0"],
        ["0", "1", "0"],
        ["0", "0", "1"],
    ]
    assert num_islands(grid) == 2


def test_merge_intervals():
    result = merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
    assert result == [[1, 6], [8, 10], [15, 18]]
