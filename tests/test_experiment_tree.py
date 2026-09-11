import sys

sys.path.insert(0, "scripts")
from experiment_tree import BST, AVLTree, node_height, SegmentTree  # noqa: E402


def test_bst_in_order_is_sorted():
    tree = BST()
    for v in [5, 3, 8, 1, 9, 4]:
        tree.insert(v)
    assert tree.in_order() == sorted([5, 3, 8, 1, 9, 4])


def test_bst_search_finds_and_misses():
    tree = BST()
    for v in [5, 3, 8]:
        tree.insert(v)
    assert tree.search(3) is True
    assert tree.search(99) is False


def test_avl_stays_balanced_on_sorted_input():
    tree = AVLTree()
    for v in range(1000):
        tree.insert(v)
    height = node_height(tree.root)
    assert height <= 2 * 10


def test_avl_matches_bst_in_order():
    values = [5, 3, 8, 1, 9, 4, 7, 2]
    bst = BST()
    avl = AVLTree()
    for v in values:
        bst.insert(v)
        avl.insert(v)

    def collect(node, out):
        if node is None:
            return
        collect(node.left, out)
        out.append(node.value)
        collect(node.right, out)

    avl_order = []
    collect(avl.root, avl_order)
    assert avl_order == bst.in_order()


def test_segment_tree_range_max():
    seg = SegmentTree([3, 7, 2, 9])
    assert seg.query(0, 1) == 7
    assert seg.query(2, 3) == 9
    assert seg.query(0, 3) == 9
    assert seg.query(1, 2) == 7


def test_segment_tree_update_changes_query():
    seg = SegmentTree([3, 7, 2, 9])
    seg.update(0, 20)
    assert seg.query(0, 1) == 20
    assert seg.query(0, 3) == 20
    assert seg.query(2, 3) == 9
