# Practice script: docs/exercise_scripts/LC146_LRUCache_practice.md
#
# NOT the version to lead with in an interview.
# Lead with the OrderedDict version (lru-cache-recommended.py).
# This file is the FOLLOW-UP that an interviewer might ask for:
# "Now do it WITHOUT collections.OrderedDict."


class Node:
    """Doubly-linked list node. Each node = one cache entry."""
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    Manual implementation: hash map + doubly-linked list.

    All operations: O(1).
    Same big-O as the OrderedDict version, just verbose. Only write this if
    the interviewer explicitly asks you to skip OrderedDict.

    Structure:
        head ←→ [most recent] ←→ ... ←→ [least recent] ←→ tail
              (head and tail are sentinel nodes — never hold real data)

        cache dict: key → Node      (gives O(1) lookup)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}    # key → Node

        # Sentinel head and tail — make insert/remove edge-case-free.
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    # ----- private helpers -----

    def _remove(self, node):
        """Unlink node from the DLL. O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        """Insert node right after the head sentinel. O(1)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    # ----- public API -----

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        # Mark as most recently used: remove + reinsert at head.
        self._remove(node)
        self._add_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing — remove from current position, will reinsert below.
            self._remove(self.cache[key])

        node = Node(key, value)
        self.cache[key] = node
        self._add_to_head(node)

        if len(self.cache) > self.capacity:
            # Evict the LRU: it's the node just before the tail sentinel.
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# ============= TEST CASES =============

cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))       # 1
cache.put(3, 3)           # evicts key 2
print(cache.get(2))       # -1
cache.put(4, 4)           # evicts key 1
print(cache.get(1))       # -1
print(cache.get(3))       # 3
print(cache.get(4))       # 4
