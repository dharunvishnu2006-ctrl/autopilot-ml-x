class HashTable:
    def __init__(self, size=16):
        self.size = size  # number of buckets
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        total = sum(ord(ch) for ch in str(key))
        return total % self.size

    def put(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False


cache2 = HashTable()
cache2.put("abc", "result_1")
cache2.put("cba", "result_2")
print(cache2.get("cba"))
print(cache2.get("xyz"))
print(cache2.delete("abc"))
print(cache2.get("abc"))
print(cache2.delete("abc"))


class HashSet:
    def __init__(self, size=16):
        self.table = HashTable(size)

    def add(self, key):
        self.table.put(key, True)

    def contains(self, key):
        return self.table.get(key) is not None

    def remove(self, key):
        return self.table.delete(key)


seen = HashSet()
config1 = "rf_depth5_lr0.01"
config2 = "xgb_depth3_lr0.1"
seen.add(config1)
print(seen.contains(config1))
print(seen.contains(config2))
seen.add(config2)
print(seen.contains(config2))


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root
        for ch in word:
            if ch not in current.children:
                current.children[ch] = TrieNode()
            current = current.children[ch]
        current.is_end = True

    def search(self, word):
        current = self.root
        for ch in word:
            if ch not in current.children:
                return False
            current = current.children[ch]
        return current.is_end


names = Trie()
names.insert("xgb_v1")
names.insert("xgb_v2")
print(names.search("xgb_v1"))
print(names.search("xgb_v3"))
print(names.search("xgb_v"))
