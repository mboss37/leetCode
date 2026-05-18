# Practice script: docs/exercise_scripts/LC146_LRUCache_practice.md

from collections import OrderedDict


class LRUCache:
    """
    LRU Cache using collections.OrderedDict.

    OrderedDict IS a hash map + linked list internally — Python's stdlib has
    already built the structure we need. Use it.

    All operations: O(1) average.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Mark this key as most recently used.
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Updating an existing key — move it to the most-recent position.
            self.cache.move_to_end(key)
        self.cache[key] = value

        # If we exceeded capacity, evict the oldest entry (the LRU one).
        # popitem(last=False) pops from the FRONT (oldest). Default is last=True.
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# ============= TEST CASES =============

cache = LRUCache(2)
cache.put(1, 1)           # cache: {1=1}
cache.put(2, 2)           # cache: {1=1, 2=2}
print(cache.get(1))       # 1 — 1 becomes most recent → {2=2, 1=1}
cache.put(3, 3)           # 2 was LRU, evicted → {1=1, 3=3}
print(cache.get(2))       # -1 (not found)
cache.put(4, 4)           # 1 was LRU, evicted → {3=3, 4=4}
print(cache.get(1))       # -1
print(cache.get(3))       # 3
print(cache.get(4))       # 4

# Edge: updating an existing key shouldn't trigger eviction
cache2 = LRUCache(2)
cache2.put(1, 1)
cache2.put(2, 2)
cache2.put(1, 99)         # update, no eviction → {2=2, 1=99}
print(cache2.get(2))      # 2
print(cache2.get(1))      # 99

# Edge: capacity = 1
cache3 = LRUCache(1)
cache3.put(1, 10)
cache3.put(2, 20)         # 1 evicted
print(cache3.get(1))      # -1
print(cache3.get(2))      # 20
