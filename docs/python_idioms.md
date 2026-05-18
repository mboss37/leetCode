# Python Idioms — Interview Fluency

> Quick reference for the patterns you reach for under pressure. Every idiom here should be muscle memory: see the signal, type the shape, move on.

---

## Quick lookup table

| When you need to… | Reach for | One-line shape |
|---|---|---|
| Walk a list with the index | `enumerate` | `for i, x in enumerate(seq):` |
| Walk two lists together | `zip` | `for a, b in zip(A, B):` |
| Count occurrences | `Counter` | `Counter(seq)` |
| Auto-create dict values | `defaultdict` | `defaultdict(list)` |
| Lookup with a default | `dict.get` | `d.get(k, default)` |
| FIFO queue (BFS) | `deque` | `dq.popleft()` |
| Priority queue / top-K | `heapq` | `heappush / heappop` |
| Substring or reverse | slicing | `s[a:b]`, `s[::-1]` |
| Build a string fast | `''.join` | `''.join(parts)` |
| Filter + transform | list comprehension | `[f(x) for x in seq if cond]` |
| Sort by a rule | `sorted(key=…)` | `sorted(xs, key=lambda x: …)` |
| Binary search in sorted | `bisect` | `bisect_left(arr, x)` |
| Set math / dedup | set operators | `a & b`, `a \| b`, `a - b` |
| Classify a char | `str.isalnum()` etc | `c.isalnum()`, `c.lower()` |
| Multiple assignment / swap | tuple unpacking | `a, b = b, a` |

---

## 1. `enumerate` — index + value in one loop

**Use:** any time you need both `i` and `nums[i]` while walking. Replace `range(len(seq))` everywhere.

```python
nums = [2, 7, 11, 15]

for i, num in enumerate(nums):
    print(f"Box {i} contains {num}")

# Start counting from 1 instead of 0:
for i, num in enumerate(nums, start=1):
    print(f"Position {i}: {num}")
```

**Convention.** Name the value after the singular of the sequence: `for i, num in enumerate(nums)`, `for i, char in enumerate(s)`. Avoids generic `v`/`x` which read worse in a whiteboard.

---

## 2. `zip` — walk two sequences in lockstep

**Use:** parallel iteration. Compare strings position-by-position, pair IDs with names, merge sorted lists.

```python
ids   = [1, 2, 3]
names = ["alice", "bob", "carol"]

for id_, name in zip(ids, names):
    print(f"{id_} -> {name}")

# Works on N sequences:
scores = [90, 85, 95]
for id_, name, score in zip(ids, names, scores):
    print(f"{id_} {name}: {score}")
```

**Gotcha.** `zip` stops at the **shortest** sequence — extras are silently dropped. If you need full coverage, use `itertools.zip_longest(seq_a, seq_b, fillvalue=…)`.

**Naming.** `id` is a built-in (returns object identity). PEP 8 says append `_` to avoid shadowing: `id_`, `type_`, `list_`.

---

## 3. `Counter` — frequency map in one line

**Use:** anagrams, frequency counts, top-K frequent. The cleanest way to count anything.

```python
from collections import Counter

c = Counter("banana")         # Counter({'a': 3, 'n': 2, 'b': 1})
c['a']                        # 3
c['z']                        # 0  ← missing keys return 0, NOT KeyError

# Top N most common:
Counter(["cat", "car", "dog", "cat"]).most_common(2)
# [('cat', 2), ('car', 1)]

# Counter equality = anagram check:
def is_anagram(s, t):
    return Counter(s) == Counter(t)

# Counter arithmetic:
Counter("aabbc") + Counter("abcc")   # Counter({'a': 3, 'b': 3, 'c': 3})
Counter("aabbc") - Counter("abcc")   # Counter({'a': 1, 'b': 1})  — negatives dropped
```

**When to use `Counter` vs `defaultdict(int)`.** Use `Counter` when counting *is* the goal — you get `.most_common()` for free and the intent is clearer. Use `defaultdict(int)` when counts are just one part of a larger structure.

---

## 4. `defaultdict` — auto-create values for missing keys

**Use:** group-by patterns. Build adjacency lists. Anything where you'd write `if k not in d: d[k] = […]; d[k].append(…)`.

```python
from collections import defaultdict

# Group by first letter
words = ["cat", "car", "dog", "cow", "dad"]
grouped = defaultdict(list)
for word in words:
    grouped[word[0]].append(word)
# {'c': ['cat', 'car', 'cow'], 'd': ['dog', 'dad']}
```

**Common factories.** `list`, `int`, `set`, `str`, or a `lambda` for custom: `defaultdict(lambda: [0, 0])`.

**Gotcha.** Accessing a missing key **creates** it.

```python
'z' in grouped         # False
_ = grouped['z']       # peeked... but this ADDED the key
'z' in grouped         # True (oops)
```

If you only want to peek without mutating, use `grouped.get('z', [])`.

---

## 5. `dict.get(key, default)` — safe lookup

**Use:** counts, lookups with fallbacks, any "key might be missing" path. No `if key in dict` dance, no `KeyError`.

```python
ages = {"alice": 30, "bob": 25}

ages.get("alice")            # 30
ages.get("charlie")          # None
ages.get("charlie", 0)       # 0

# Counting with plain dict:
counts = {}
for c in "hello":
    counts[c] = counts.get(c, 0) + 1
# {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

**Trap.** Default 0 gives correct counting (`0 + 1 = 1` on first sight). `.get(c, 1) + 1` would give 2 on first sight — off-by-one.

**`.get` vs `defaultdict`.** `.get` is read-only — doesn't mutate. `defaultdict` mutates on first access. For pure lookups, `.get`. For build-and-accumulate, `defaultdict`.

---

## 6. `collections.deque` — O(1) at both ends

**Use:** BFS queues. Sliding windows. Anything where `list.pop(0)` would be O(n).

```python
from collections import deque

dq = deque()
dq.append(1)        # right
dq.appendleft(0)    # left
dq.pop()            # remove from right
dq.popleft()        # remove from LEFT — the killer feature

# Initialize from an iterable:
deque([1, 2, 3, 4])

# Bounded — drops from opposite end when full:
window = deque(maxlen=3)
for n in [1, 2, 3, 4, 5]:
    window.append(n)
# After all appends: deque([3, 4, 5], maxlen=3)
```

**Why not a list?** `list.pop(0)` shifts every other element → O(n). `deque.popleft()` is O(1).

**BFS template:**

```python
def bfs(start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**Gotcha.** Random indexing (`dq[5]`) works but is O(n). For indexing, use a list.

---

## 7. `heapq` — priority queue / top-K

**Use:** top-K largest/smallest, scheduling by priority, K-way merge.

```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)

heap[0]                # 2 — peek smallest, O(1)
heapq.heappop(heap)    # 2 — remove smallest, O(log n)

# Heapify an existing list — O(n):
nums = [5, 2, 8, 1, 7]
heapq.heapify(nums)    # mutates in place
```

**Min-heap only.** Python has no native max-heap. Negate values to fake it:

```python
nums = [5, 2, 8, 1, 7]
max_heap = [-n for n in nums]
heapq.heapify(max_heap)
-heapq.heappop(max_heap)   # 8 — largest (negate back)
```

**Top-K pattern.** Keep a min-heap of size K. Smaller-than-root candidates can be skipped; root = K-th element overall.

```python
def top_k(nums, k):
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)        # drop smallest
    return sorted(heap, reverse=True)  # what survives = top K
```

This is O(n log k) — beats sorting (O(n log n)) when k ≪ n.

**Tuples for priority:** heaps compare element-wise. `(priority, item)` works because the priority is compared first.

```python
tasks = []
heapq.heappush(tasks, (3, "low"))
heapq.heappush(tasks, (1, "URGENT"))
heapq.heappop(tasks)   # (1, 'URGENT')
```

**Shortcuts.** `heapq.nlargest(k, seq)` / `nsmallest(k, seq)`. Fine to use unless asked to implement.

---

## 8. Slicing — `s[a:b]`, `s[::-1]`, `s[::step]`

**Use:** substrings, reversals, every-other patterns. Works identically on strings and lists.

```python
s = "hello world"

s[0:5]      # "hello"        — indices 0..4 (5 NOT included)
s[6:]       # "world"        — from 6 to end
s[:5]       # "hello"        — start to 5
s[:]        # "hello world"  — full copy

s[::-1]     # "dlrow olleh"  — reverse
s[::2]      # "hlowrd"       — every other char

s[-5:]      # "world"        — last 5
s[:-6]      # "hello"        — everything except last 6
```

**Slicing creates a new object — original is unchanged.** Different from `list.reverse()` which mutates.

**Slices never throw.** Out-of-range silently clamps to empty.

```python
"hello"[100:200]    # ""   — no error
nums[10:]           # []   — no error
# But: nums[10]  →  IndexError
```

**Palindrome one-liner:** `return s == s[::-1]`.

---

## 9. `''.join(iterable)` — fast string building

**Use:** anywhere you'd otherwise do `result += char` in a loop. Always.

```python
parts = ["hello", " ", "world"]
''.join(parts)                  # "hello world"
', '.join(["a", "b", "c"])      # "a, b, c"

# Filter + map + join — the canonical "clean a string" line:
text = "Hello, World!"
cleaned = ''.join(c.lower() for c in text if c.isalnum())
# "helloworld"
```

**Why not `+=`?** Strings are immutable. `result += char` in a loop allocates a new string each iteration → O(n²) total. `''.join` is O(n) — single allocation.

**Items must be strings.** `''.join([1, 2, 3])` raises TypeError. Convert first:

```python
''.join(str(n) for n in [1, 2, 3])   # "123"
```

---

## 10. List / set / dict comprehensions

**Use:** filter + transform in one expression. Read left-to-right backwards: *"for each x in seq, if condition, include expr."*

```python
nums = [1, 2, 3, 4, 5]

[n * n for n in nums]                  # [1, 4, 9, 16, 25]
[n for n in nums if n % 2 == 0]        # [2, 4]
[n * n for n in nums if n % 2 == 0]    # [4, 16]

# if-else inside the expression (different from the filter):
["even" if n % 2 == 0 else "odd" for n in nums]

# Set + dict comprehensions:
{len(w) for w in ["cat", "car", "dog", "bird"]}     # {3, 4}
{w: len(w) for w in ["cat", "bird"]}                # {'cat': 3, 'bird': 4}
```

**Don't nest deeply.** If you need more than 2 `for` clauses or branched logic, write a real `for` loop. Readability beats compactness.

---

## 11. `sorted(seq, key=…)` — custom sort

**Use:** sort by a derived value, multiple keys, or descending.

```python
sorted(nums)                  # ascending (default)
sorted(nums, reverse=True)    # descending

# Sort by length:
sorted(words, key=len)

# Sort dicts by a field:
people = [{"name": "alice", "age": 30}, {"name": "bob", "age": 25}]
sorted(people, key=lambda p: p["age"])

# Multi-key (tuple) — age ascending, name as tiebreaker:
sorted(people, key=lambda p: (p["age"], p["name"]))
```

**`sorted()` vs `.sort()`.** `sorted()` returns a new list. `.sort()` mutates in place and returns `None`. Don't write `x = nums.sort()` — `x` becomes `None`.

**Group Anagrams trick.** Sorting each string gives a canonical anagram key:

```python
''.join(sorted("eat"))   # "aet"
''.join(sorted("tea"))   # "aet"   — same key → same group
```

**Gotcha.** Strings sort by codepoint, so uppercase comes before lowercase. For case-insensitive, use `key=str.lower`.

---

## 12. `bisect` — binary search without writing it

**Use:** find an insertion point in a sorted list. Skip the off-by-one headache.

```python
from bisect import bisect_left, bisect_right, insort

nums = [1, 3, 5, 5, 5, 7, 9]
#       0  1  2  3  4  5  6

bisect_left(nums, 5)    # 2  — first 5 is at index 2
bisect_right(nums, 5)   # 5  — first slot AFTER the last 5
bisect_left(nums, 4)    # 2  — where 4 would go
bisect_left(nums, 0)    # 0  — before everything
bisect_left(nums, 10)   # 7  — past the end
```

**First AND last occurrence pattern (LC 34):**

```python
first = bisect_left(nums, target)
last  = bisect_right(nums, target) - 1
if first <= last and nums[first] == target:
    return [first, last]
return [-1, -1]
```

**`insort`** inserts in sorted order, mutating the list.

**Interview note.** Some interviewers want you to write the binary search yourself. Be ready to do both — `bisect` for fluency, manual for understanding.

---

## 13. Set operations

**Use:** dedup, "what's common", "what's only in one", fast `in` checks.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b      # {1, 2, 3, 4, 5, 6}   — union
a & b      # {3, 4}               — intersection
a - b      # {1, 2}               — in a but NOT b
a ^ b      # {1, 2, 5, 6}         — in either but NOT both

# Build from any iterable:
set("hello")           # {'h', 'e', 'l', 'o'}    — duplicates collapsed
set([1, 2, 2, 3])      # {1, 2, 3}

# Membership: O(1) average
3 in {1, 2, 3, 4, 5}   # True

# Subset:
{1, 2}.issubset({1, 2, 3})   # True
{1, 2} <= {1, 2, 3}          # True (operator form)
```

**`set` vs `list` for membership.** `x in [...]` is O(n). `x in {...}` is O(1). This is why Contains Duplicate uses a set.

**Gotcha.** `{}` is an empty **dict**, not an empty set. Use `set()`.

**Members must be hashable.** Tuples OK, lists not OK:

```python
{(1, 2), (3, 4)}   # ✓
{[1, 2], [3, 4]}   # ✗  TypeError: unhashable type: 'list'
```

---

## 14. String predicates — `.isalnum`, `.isalpha`, `.isdigit`, `.lower`, `.upper`

**Use:** Valid Palindrome–style "ignore spaces/punctuation" filters. String normalization.

```python
"a".isalnum()      # True
"3".isalnum()      # True
" ".isalnum()      # False
"a3".isalnum()     # True   — works on whole strings (every char must qualify)

"hello".isalpha()  # True
"hello3".isalpha() # False

"123".isdigit()    # True
"1.5".isdigit()    # False  — '.' disqualifies

# Case conversion — returns a NEW string:
"Hello".lower()    # "hello"
"Hello".upper()    # "HELLO"
```

**The canonical "clean a string" idiom:**

```python
cleaned = ''.join(c.lower() for c in text if c.isalnum())
```

Filter (`isalnum`) + map (`.lower`) + join — one line, used in every palindrome and anagram problem.

**Gotcha.** Empty string returns `False` for every `is*` predicate — they require at least one char.

---

## 15. Tuple unpacking

**Use:** multiple assignment, swaps, capturing multi-return, iterating pairs.

```python
a, b = 1, 2                           # a=1, b=2
a, b = b, a                           # swap — no temp variable needed
a, b, c = [10, 20, 30]                # works on any iterable of matching length

# Initialize two pointers:
left, right = 0, len(nums) - 1

# Multi-return:
def divmod_simple(a, b):
    return a // b, a % b

q, r = divmod_simple(17, 5)           # 3, 2

# Star unpacking — "the rest":
first, *rest = [1, 2, 3, 4, 5]        # first=1, rest=[2, 3, 4]
*head, last  = [1, 2, 3, 4, 5]        # head=[1, 2, 3, 4], last=5
first, *mid, last = [1, 2, 3, 4, 5]   # first=1, mid=[2, 3], last=5
```

**Used everywhere implicitly:**

```python
for i, x   in enumerate(seq): ...     # (index, value) tuple
for a, b   in zip(A, B):      ...     # (a, b) tuple
for k, v   in d.items():      ...     # (key, value) tuple
```

**Gotcha.** Length on the left must match (without `*`) the right:

```python
a, b = [1, 2, 3]      # ValueError: too many values
a, b, c = [1, 2]      # ValueError: not enough values
```

---

## How to drill these

1. Pick one idiom from the table above.
2. Read this page's section — out loud helps.
3. Close it.
4. Open a blank scratch buffer.
5. Type the canonical form from memory.
6. Run it. Compare.
7. If wrong: log the weak spot. Retype it tomorrow.

Five minutes per idiom. The whole list goes from "I think I remember" to muscle memory in a week of daily passes.

---

## Chain back to the problems

| Idiom | Where it shows up |
|---|---|
| `enumerate` | Two Sum, almost every array walk |
| `Counter` | Valid Anagram, Top K Frequent, Group Anagrams |
| `defaultdict(list)` | Group Anagrams, adjacency-list builds |
| `set` | Contains Duplicate, Longest Consecutive Sequence, Word Search visited |
| `deque` | Binary Tree Level Order, Number of Islands, BFS in general |
| `heapq` | Top K Frequent Elements (alternative path) |
| slicing | Valid Palindrome, Longest Palindromic Substring, Merge Strings Alternately |
| `''.join` | Group Anagrams (canonical key), every string-building problem |
| `sorted(key=…)` | Group Anagrams, Merge Intervals |
| `bisect` | Search Insert Position, Find First and Last Position |
| tuple unpacking | every two-pointer init, every `dict.items()` walk |
| string predicates | Valid Palindrome |
