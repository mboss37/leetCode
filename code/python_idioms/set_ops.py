# Idiom: set operations (union, intersection, difference, symmetric_difference)
# Use: math on collections — find what's common, what's only in one, etc.
# Canonical forms:
#     a | b        -> union (everything in either)
#     a & b        -> intersection (in BOTH)
#     a - b        -> difference (in a, NOT in b)
#     a ^ b        -> symmetric difference (in either, NOT both)

# === Basic set creation ===

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# === Union — everything in either set ===

print(a | b)              # {1, 2, 3, 4, 5, 6}
print(a.union(b))         # same — method form

# === Intersection — only items in BOTH ===

print(a & b)              # {3, 4}
print(a.intersection(b))  # same

# === Difference — items in a but NOT in b ===

print(a - b)              # {1, 2}
print(a.difference(b))    # same

# Order matters for difference:
print(b - a)              # {5, 6}

# === Symmetric difference — items in EITHER but NOT both ===

print(a ^ b)                          # {1, 2, 5, 6}
print(a.symmetric_difference(b))      # same

# Useful for "what's different between these two collections"

# === Membership: O(1) average lookup ===

s = {1, 2, 3, 4, 5}
print(3 in s)             # True
print(99 in s)            # False
# Same O(1) magic as dict.

# === Build a set from any iterable ===

print(set("hello"))           # {'h', 'e', 'l', 'o'}    (duplicates collapsed)
print(set([1, 2, 2, 3, 3]))   # {1, 2, 3}
print(set(range(5)))          # {0, 1, 2, 3, 4}

# === Common interview uses ===

# Dedup a list (loses order!):
nums = [1, 2, 2, 3, 3, 3, 4]
print(list(set(nums)))    # [1, 2, 3, 4]  (order may vary)

# Quick "do these have anything in common?" check:
print(bool({1, 2, 3} & {3, 4, 5}))   # True   — 3 is shared
print(bool({1, 2} & {3, 4}))         # False  — disjoint

# Check subset:
print({1, 2}.issubset({1, 2, 3}))     # True
print({1, 2} <= {1, 2, 3})            # True   — same thing with operator

# === Sets vs lists for "have I seen this?" check ===

# List:  `x in [...]`   is O(n)  — walks the whole list
# Set:   `x in {...}`   is O(1)  — hash lookup

# This is why Contains Duplicate uses a set, not a list.

# === Gotcha ===

# `{}` is an empty DICT, not an empty set. To create an empty set: `set()`.
empty_dict = {}
empty_set = set()
print(type(empty_dict))   # <class 'dict'>
print(type(empty_set))    # <class 'set'>

# Set members must be IMMUTABLE (just like dict keys).
# {1, 2, 3}             ✓
# {(1, 2), (3, 4)}      ✓   (tuples are immutable)
# {[1, 2], [3, 4]}      ✗   TypeError: unhashable type: 'list'
