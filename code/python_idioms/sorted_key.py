# Idiom: sorted(seq, key=...)
# Use: sort a sequence by a CUSTOM rule, not the default natural order.
# Canonical form:
#     sorted(seq, key=lambda x: ...)
#     sorted(seq, key=function_name)
#     sorted(seq, reverse=True)         -> descending instead of ascending

# === Basic sort (no key) ===

nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(nums))              # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(nums, reverse=True))# [9, 6, 5, 4, 3, 2, 1, 1]

words = ["banana", "apple", "cherry"]
print(sorted(words))             # ['apple', 'banana', 'cherry']  — alphabetical by default

# === Custom key — sort by string length ===

print(sorted(words, key=len))    # ['apple', 'banana', 'cherry']  — by length (5, 6, 6)

# Different sort:
words2 = ["aaa", "b", "cc"]
print(sorted(words2, key=len))   # ['b', 'cc', 'aaa']

# === Custom key with lambda — sort by last character ===

print(sorted(words, key=lambda w: w[-1]))   # ['banana', 'apple', 'cherry']
#                                              ends in: a, e, y — sorted by last char

# === Sort dicts / tuples by a specific field ===

people = [
    {"name": "alice", "age": 30},
    {"name": "bob", "age": 25},
    {"name": "carol", "age": 35},
]

# By age
print(sorted(people, key=lambda p: p["age"]))
# [{'name': 'bob', 'age': 25}, {'name': 'alice', 'age': 30}, {'name': 'carol', 'age': 35}]

# By name
print(sorted(people, key=lambda p: p["name"]))
# [{'name': 'alice', ...}, {'name': 'bob', ...}, {'name': 'carol', ...}]

# === Sort by multiple keys (tuple key) ===

# Sort by age ascending, then name alphabetical as tiebreaker
print(sorted(people, key=lambda p: (p["age"], p["name"])))

# === sorted() vs .sort() ===

# sorted() — returns a NEW list. Original unchanged.
nums = [3, 1, 4]
new = sorted(nums)
print(nums)   # [3, 1, 4]   — unchanged
print(new)    # [1, 3, 4]

# .sort() — mutates the list IN PLACE. Returns None.
nums = [3, 1, 4]
nums.sort()
print(nums)   # [1, 3, 4]   — mutated

# === Common interview use ===

# Group Anagrams (LC 49): sort each string to get a canonical key
words = ["eat", "tea", "ate", "tan", "nat"]
for w in words:
    print(w, "->", ''.join(sorted(w)))
# eat -> aet
# tea -> aet
# ate -> aet
# tan -> ant
# nat -> ant
# Anagrams share the same sorted key.

# === Gotcha ===
# Strings sort by Unicode codepoint, which means UPPERCASE comes BEFORE LOWERCASE.
print(sorted(["banana", "Apple", "cherry"]))    # ['Apple', 'banana', 'cherry']
# To sort case-insensitively:
print(sorted(["banana", "Apple", "cherry"], key=str.lower))
# ['Apple', 'banana', 'cherry']   — same here but the comparison is case-insensitive
