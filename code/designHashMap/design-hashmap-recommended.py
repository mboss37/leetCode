# Practice script: docs/exercise_scripts/LC706_DesignHashMap_practice.md

from typing import List, Tuple


class MyHashMap:
    """A toy hash map built with separate chaining.

    We pick a fixed number of buckets. Each bucket is a list of (key, value)
    pairs. To find/insert/remove a key:
      1. Hash key -> bucket index (just modulo).
      2. Linear scan the small bucket list.

    Average O(1) when keys are well-distributed and buckets are small.
    Worst case O(n) if everything hashes to one bucket.
    """

    def __init__(self):
        self.size = 1000
        self.buckets: List[List[Tuple[int, int]]] = [[] for _ in range(self.size)]

    def _bucket(self, key: int) -> List[Tuple[int, int]]:
        return self.buckets[key % self.size]

    def put(self, key: int, value: int) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)   # update existing
                return
        bucket.append((key, value))         # new entry

    def get(self, key: int) -> int:
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return


# ============= TEST CASES =============
m = MyHashMap()
m.put(1, 1)
m.put(2, 2)
print(m.get(1))     # 1
print(m.get(3))     # -1 (not found)
m.put(2, 1)         # update
print(m.get(2))     # 1
m.remove(2)
print(m.get(2))     # -1 (removed)
