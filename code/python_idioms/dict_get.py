# Idiom: dict.get(key, default)
# Use: look up a key in a dict, return a default if the key isn't there.
#      No exception, no KeyError, no need for `if key in dict` checks.
# Canonical form:
#     value = my_dict.get(key, default_value)

# === Basic form ===

ages = {"alice": 30, "bob": 25}

# Key exists — returns the value
print(ages.get("alice"))         # 30

# Key MISSING — without default: returns None
print(ages.get("charlie"))       # None

# Key MISSING — with default: returns the default
print(ages.get("charlie", 0))    # 0
print(ages.get("charlie", "?"))  # "?"

# Compare to direct indexing:
# ages["charlie"]    -> KeyError: 'charlie'  (crashes)

# === Common pattern: counting ===

# Build a frequency map of characters in a string:
counts = {}
for c in "hello":
    counts[c] = counts.get(c, 0) + 1
#                            ^ default 0 for never-seen chars

print(counts)   # {'h': 1, 'e': 1, 'l': 2, 'o': 1}

# CRITICAL TRAP: the default is the value PRETENDED to be there BEFORE this sighting.
# For counting starting at 1 on first sight: default = 0 (so 0 + 1 = 1).
# If you wrote .get(c, 1) + 1, first sight would become 2 — off-by-one bug.

# === Why this is cleaner than `if key in dict` ===

# Verbose (don't write this):
counts = {}
for c in "hello":
    if c in counts:
        counts[c] = counts[c] + 1
    else:
        counts[c] = 1

# Same result with .get():
counts = {}
for c in "hello":
    counts[c] = counts.get(c, 0) + 1

# === defaultdict is even cleaner for counting ===

# If counting is the WHOLE point, use defaultdict(int):
from collections import defaultdict

counts = defaultdict(int)
for c in "hello":
    counts[c] += 1
#   ^ no .get() needed — defaultdict auto-creates keys at 0

# === Gotcha ===

# .get() does NOT add the key to the dict. Only .get + assign does.
d = {}
d.get("x", 0)        # returns 0 — but does NOT add "x" to d
print(d)             # {}        — d is still empty

d["x"] = d.get("x", 0) + 1
print(d)             # {'x': 1}  — now "x" is in d
