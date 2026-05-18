# Idiom: defaultdict
# Use: dictionary that auto-creates a default value for any missing key.
# Canonical form:
#     from collections import defaultdict
#     d = defaultdict(<factory>)
# Common factories: list, int, set, str, lambda: <custom>

from collections import defaultdict

# Group words by their first letter.
words = ["cat", "car", "dog", "cow", "dad"]

grouped = defaultdict(list)
for word in words:
    grouped[word[0]].append(word)

print(dict(grouped))
# Expected: {'c': ['cat', 'car', 'cow'], 'd': ['dog', 'dad']}

# Why defaultdict beats a plain dict here:
# With a plain dict you'd need a check-and-init dance every time:
#     if word[0] not in grouped:
#         grouped[word[0]] = []
#     grouped[word[0]].append(word)
# defaultdict skips that — the first time you touch a missing key,
# the factory (`list`) runs and gives you an empty list automatically.

# Count occurrences (Counter is usually better, but defaultdict(int) works).
counts = defaultdict(int)
for word in words:
    counts[word[0]] += 1
print(dict(counts))
# Expected: {'c': 3, 'd': 2}

# Track unique items per group with a set:
seen_per_letter = defaultdict(set)
for word in words:
    seen_per_letter[word[0]].add(word)
print({k: sorted(v) for k, v in seen_per_letter.items()})
# Expected: {'c': ['car', 'cat', 'cow'], 'd': ['dad', 'dog']}

# Gotcha: accessing a missing key CREATES it.
# So `grouped['z']` returns [] AND adds 'z' to grouped with an empty list as value.
# If you want to peek without mutating, use grouped.get('z', []).
print('z' in grouped)         # False
_ = grouped['z']              # peeked — but this ADDS the key
print('z' in grouped)         # True (oops)
