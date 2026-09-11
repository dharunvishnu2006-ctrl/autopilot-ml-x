import sys

sys.path.insert(0, "scripts")
from feature_cache import HashTable, HashSet, Trie  # noqa: E402


def test_hashtable_put_get_matches_dict():
    ht = HashTable()
    ref = {}
    pairs = [("a", 1), ("b", 2), ("c", 3), ("a", 9)]
    for k, v in pairs:
        ht.put(k, v)
        ref[k] = v
    for k in ref:
        assert ht.get(k) == ref[k]


def test_hashtable_survives_collision():
    ht = HashTable(size=1)
    ht.put("x", "val_x")
    ht.put("y", "val_y")
    assert ht.get("x") == "val_x"
    assert ht.get("y") == "val_y"


def test_hashtable_delete_removes_key():
    ht = HashTable()
    ht.put("k", "v")
    assert ht.delete("k") is True
    assert ht.get("k") is None
    assert ht.delete("k") is False


def test_hashset_membership():
    s = HashSet()
    s.add("cfg_1")
    assert s.contains("cfg_1") is True
    assert s.contains("cfg_2") is False
    s.remove("cfg_1")
    assert s.contains("cfg_1") is False


def test_trie_exact_word_vs_prefix():
    t = Trie()
    t.insert("model_a")
    t.insert("model_ab")
    assert t.search("model_a") is True
    assert t.search("model_ab") is True
    assert t.search("model") is False
    assert t.search("model_x") is False
