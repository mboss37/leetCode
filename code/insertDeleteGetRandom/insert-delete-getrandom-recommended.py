# Practice script: docs/exercise_scripts/LC380_InsertDeleteGetRandom_practice.md

import random


class RandomizedSet:
    """O(1) insert / remove / getRandom.

    Trick: keep TWO structures in sync:
      - items: dynamic array (list). Fast random access by index.
      - idx:   dict {value -> position in items}. Fast lookup of "where is val?"

    Insert is just list.append + dict update.

    Remove is the clever bit: to remove from a list in O(1), you SWAP the
    target with the last element, then pop the last. The dict tells you
    the target's index, and you update the swapped element's index.

    getRandom is random.choice on the list — uniform and O(1).
    """

    def __init__(self):
        self.items = []          # values in arbitrary order
        self.idx = {}            # value -> index in self.items

    def insert(self, val: int) -> bool:
        if val in self.idx:
            return False
        self.idx[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.idx:
            return False
        # Swap target with last element so we can pop in O(1).
        i = self.idx[val]
        last_val = self.items[-1]
        self.items[i] = last_val
        self.idx[last_val] = i
        self.items.pop()
        del self.idx[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.items)


# ============= TEST CASES =============
rs = RandomizedSet()
print(rs.insert(1))      # True
print(rs.remove(2))      # False — not present
print(rs.insert(2))      # True
print(rs.getRandom())    # 1 or 2
print(rs.remove(1))      # True
print(rs.insert(2))      # False — already in
print(rs.getRandom())    # 2

# Bigger test
rs2 = RandomizedSet()
for x in [10, 20, 30, 40, 50]:
    rs2.insert(x)
rs2.remove(30)
print(sorted(rs2.items))    # [10, 20, 40, 50]
