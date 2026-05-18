# Idiom: Counter
# Use: count occurrences of items in a sequence. Returns a dict-like object.
# Canonical form:
#     from collections import Counter
#     c = Counter(seq)

from collections import Counter

# Letter frequency:
c = Counter("banana")
print(c)
# Expected: Counter({'a': 3, 'n': 2, 'b': 1})

print(c['a'])   # 3
print(c['z'])   # 0  <- missing keys return 0, NOT a KeyError

# Word frequency:
words = ["cat", "car", "dog", "cat", "car", "cat"]
wc = Counter(words)
print(wc)
# Expected: Counter({'cat': 3, 'car': 2, 'dog': 1})

# Top N most common:
print(wc.most_common(2))
# Expected: [('cat', 3), ('car', 2)]

# Iterate like a dict:
for word, count in wc.items():
    print(f"{word}: {count}")

# Counter arithmetic:
a = Counter("aabbc")
b = Counter("abcc")
print(a + b)
# Expected: Counter({'a': 3, 'b': 3, 'c': 3})

print(a - b)
# Expected: Counter({'a': 1, 'b': 1})
# Negative or zero counts are dropped.

# Equality check — this is the cleanest anagram test in Python:
def is_anagram(s, t):
    return Counter(s) == Counter(t)

print(is_anagram("listen", "silent"))   # True
print(is_anagram("hello", "world"))     # False

# Why use Counter instead of defaultdict(int)?
# 1. Counter accepts any iterable directly: Counter("banana"), Counter([1,2,2,3]).
# 2. Missing keys return 0 (defaultdict(int) does too, but Counter is more idiomatic for counts).
# 3. Built-in .most_common(n) is very useful for "top K" problems.
# Use Counter when the goal IS counting. Use defaultdict for everything else.
