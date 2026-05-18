# Idiom: tuple unpacking
# Use: assign multiple variables in one line. Swap values. Capture multiple
#      return values cleanly. Iterate over pairs.
# Canonical forms:
#     a, b = 1, 2                    -> a=1, b=2
#     a, b = b, a                    -> swap without a temp variable
#     first, *rest = [1, 2, 3, 4]    -> first=1, rest=[2, 3, 4]

# === Basic multiple assignment ===

a, b = 1, 2
print(a, b)        # 1 2

# Works for any iterable of matching length:
a, b, c = [10, 20, 30]
print(a, b, c)     # 10 20 30

a, b, c = "xyz"
print(a, b, c)     # x y z

# === Swap idiom (no temp variable needed) ===

# Old-school swap:
# tmp = a
# a = b
# b = tmp

# Pythonic swap (one line):
a, b = 5, 10
a, b = b, a
print(a, b)        # 10 5

# Used heavily in two-pointer problems:
# left, right = right, left   (rarely useful directly, but the syntax is the same idea)

# === Initialize two-pointer pattern ===

# Common in Two Sum Sorted, 3Sum, Binary Search:
nums = [1, 2, 3, 4, 5]
left, right = 0, len(nums) - 1
print(left, right)   # 0 4

# === Capture multiple return values ===

def divmod_simple(a, b):
    return a // b, a % b   # returns a TUPLE

q, r = divmod_simple(17, 5)
print(q, r)        # 3 2

# Standard library has divmod() built in:
print(divmod(17, 5))   # (3, 2) — a tuple

# === enumerate(), zip(), dict.items() — all use unpacking ===

names = ["alice", "bob", "carol"]

# enumerate yields (index, value) tuples:
for i, name in enumerate(names):
    print(i, name)
# 0 alice
# 1 bob
# 2 carol

# zip yields (a, b) tuples:
ages = [30, 25, 35]
for name, age in zip(names, ages):
    print(name, age)
# alice 30
# bob 25
# carol 35

# dict.items() yields (key, value) tuples:
d = {"a": 1, "b": 2}
for key, value in d.items():
    print(key, value)
# a 1
# b 2

# === Star unpacking (* for "the rest") ===

first, *rest = [1, 2, 3, 4, 5]
print(first)       # 1
print(rest)        # [2, 3, 4, 5]

*head, last = [1, 2, 3, 4, 5]
print(head)        # [1, 2, 3, 4]
print(last)        # 5

first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)   # 1 [2, 3, 4] 5

# === Gotcha ===

# Number of variables on the left MUST match (without *) the length on the right.
# a, b = [1, 2, 3]    -> ValueError: too many values to unpack
# a, b, c = [1, 2]    -> ValueError: not enough values to unpack
