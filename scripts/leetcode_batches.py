def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return None


def contains_duplicate(nums):
    return len(set(nums)) != len(nums)


def intersection(a, b):
    return list(set(a) & set(b))


print(two_sum([2, 7, 11, 15], 9))
print(contains_duplicate([1, 2, 3, 1]))
print(contains_duplicate([1, 2, 3]))
print(sorted(intersection([1, 2, 3], [2, 3, 4])))


def valid_parentheses(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack.pop() != pairs[ch]:
                return False
    return len(stack) == 0


def climbing_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


print(valid_parentheses("([)]"))
print(valid_parentheses("([{}])"))
print(climbing_stairs(5))


def max_subarray(nums):
    best = nums[0]
    current = nums[0]
    for n in nums[1:]:
        current = max(n, current + n)
        best = max(best, current)
    return best


def move_zeroes(nums):
    pos = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[pos], nums[i] = nums[i], nums[pos]
            pos += 1
    return nums


print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
print(move_zeroes([0, 1, 0, 3, 12]))


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


def reverse_linked_list(head):
    prev = None
    current = head
    while current is not None:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev


def has_cycle(head):
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


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
print(result)

n2.next = n1
print(has_cycle(n1))

c1 = ListNode(1)
c2 = ListNode(2)
c3 = ListNode(3)
c1.next = c2
c2.next = c3
c3.next = c1
print(has_cycle(c1))

c4 = ListNode(1)
c5 = ListNode(2)
c4.next = c5
print(has_cycle(c4))


def longest_substring_no_repeat(s):
    seen = set()
    left = 0
    best = 0

    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        best = max(best, right - left + 1)
    return best


print(longest_substring_no_repeat("abcabcbb"))
print(longest_substring_no_repeat("bbbbb"))
print(longest_substring_no_repeat("pwwkew"))


def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != float("inf") else -1


print(coin_change([1, 2, 5], 11))
print(coin_change([2], 3))


def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def flood(r, c):
        stack = [(r, c)]
        while stack:
            row, col = stack.pop()
            if (row, col) in visited:
                continue
            if row < 0 or row >= rows or col < 0 or col >= cols:
                continue  # off the grid
            if grid[row][col] != "1":
                continue
            visited.add((row, col))
            stack.extend(
                [
                    (row + 1, col),
                    (row - 1, col),
                    (row, col + 1),
                    (row, col - 1),
                ]
            )

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visited:
                flood(r, c)
                count += 1
    return count


grid = [
    ["1", "1", "0"],
    ["0", "1", "0"],
    ["0", "0", "1"],
]
print(num_islands(grid))


def merge_intervals(intervals):
    ordered = sorted(intervals, key=lambda pair: pair[0])
    merged = [ordered[0]]

    for start, end in ordered[1:]:
        last_end = merged[-1][1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
    return merged


print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))
