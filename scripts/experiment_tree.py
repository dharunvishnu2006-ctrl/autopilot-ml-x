import random


class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return BSTNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        return node

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node is None:
            return
        self._in_order(node.left, result)
        result.append(node.value)
        self._in_order(node.right, result)


tree = BST()
for v in [5, 3, 8, 1]:
    tree.insert(v)
print(tree.root.value)
print(tree.root.left.value)
print(tree.root.left.left.value)
print(tree.root.right.value)

print(tree.search(8))
print(tree.search(99))
print(tree.in_order())


def tree_height(node):
    if node is None:
        return 0
    left_h = tree_height(node.left)
    right_h = tree_height(node.right)
    return 1 + max(left_h, right_h)


sorted_tree = BST()
for v in range(500):
    sorted_tree.insert(v)
print("sorted-insert height:", tree_height(sorted_tree.root))

shuffled = list(range(500))
random.shuffle(shuffled)
random_tree = BST()
for v in shuffled:
    random_tree.insert(v)
print("random-insert height:", tree_height(random_tree.root))


class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


def node_height(node):
    return node.height if node else 0


def balance_factor(node):
    return node_height(node.left) - node_height(node.right)


def update_height(node):
    left_h = node_height(node.left)
    right_h = node_height(node.right)
    node.height = 1 + max(left_h, right_h)


def rotate_left(node):
    new_root = node.right
    node.right = new_root.left
    new_root.left = node
    update_height(node)
    update_height(new_root)
    return new_root


def rotate_right(node):
    new_root = node.left
    node.left = new_root.right
    new_root.right = node
    update_height(node)
    update_height(new_root)
    return new_root


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        update_height(node)
        bf = balance_factor(node)
        if bf > 1 and value < node.left.value:
            return rotate_right(node)
        if bf < -1 and value > node.right.value:
            return rotate_left(node)
        if bf > 1 and value > node.left.value:
            node.left = rotate_left(node.left)
            return rotate_right(node)
        if bf < -1 and value < node.right.value:
            node.right = rotate_right(node.right)
            return rotate_left(node)
        return node


avl_tree = AVLTree()
for v in range(2000):
    avl_tree.insert(v)
print("AVL sorted-insert height:", node_height(avl_tree.root))


class SegmentTree:
    def __init__(self, values):
        self.n = len(values)
        self.tree = [0] * (4 * self.n)
        self._build(values, 0, 0, self.n - 1)

    def _build(self, values, node, lo, hi):
        if lo == hi:
            self.tree[node] = values[lo]
            return
        mid = (lo + hi) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        self._build(values, left_child, lo, mid)
        self._build(values, right_child, mid + 1, hi)
        self.tree[node] = max(self.tree[left_child], self.tree[right_child])

    def query(self, left, right):
        return self._query(0, 0, self.n - 1, left, right)

    def _query(self, node, lo, hi, left, right):
        if right < lo or hi < left:
            return float("-inf")
        if left <= lo and hi <= right:
            return self.tree[node]
        mid = (lo + hi) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        left_max = self._query(left_child, lo, mid, left, right)
        right_max = self._query(right_child, mid + 1, hi, left, right)
        return max(left_max, right_max)

    def update(self, index, value):
        self._update(0, 0, self.n - 1, index, value)

    def _update(self, node, lo, hi, index, value):
        if lo == hi:
            self.tree[node] = value
            return
        mid = (lo + hi) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        if index <= mid:
            self._update(left_child, lo, mid, index, value)
        else:
            self._update(right_child, mid + 1, hi, index, value)
        self.tree[node] = max(self.tree[left_child], self.tree[right_child])


seg = SegmentTree([3, 7, 2, 9])
print(seg.tree[:7])

print(seg.query(0, 1))
print(seg.query(2, 3))
print(seg.query(0, 3))
print(seg.query(1, 2))

seg.update(0, 20)
print(seg.query(0, 1))
print(seg.query(0, 3))
print(seg.query(2, 3))
