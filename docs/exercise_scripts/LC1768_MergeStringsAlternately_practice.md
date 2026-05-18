# LC 1768 — Merge Strings Alternately · Practice Script

**Code:** [code/mergeStringsAlternately/](../../code/mergeStringsAlternately/)

---

## Problem

> Given two strings `word1` and `word2`, merge them by adding letters in **alternating order**, starting with `word1`. If one string is longer, append the rest at the end.

**Examples:**
- `"abc" + "pqr" → "apbqcr"`
- `"ab" + "pqrs" → "apbqrs"`
- `"abcd" + "pq" → "apbqcd"`

**Constraints:**
- `1 <= word1.length, word2.length <= 100`

---

## RECOMMENDED — Two Pointers + tail append (O(n + m))

```python
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        out = []
        i, j = 0, 0
        while i < len(word1) and j < len(word2):
            out.append(word1[i])
            out.append(word2[j])
            i += 1
            j += 1
        out.append(word1[i:])   # tail of word1 (empty if exhausted)
        out.append(word2[j:])   # tail of word2 (empty if exhausted)
        return ''.join(out)
```

### The key idea

Walk both strings together. Each round: take one char from `word1`, then one from `word2`. When one runs out, append whatever's left of the other.

Python slicing makes this clean: **`word[i:]` is the empty string if `i >= len(word)`**, so you can append both tails unconditionally — exactly one of them is non-empty (or both are empty).

### Why `''.join(list)` and not `+=`

Strings are immutable in Python. Doing `result += char` builds a new string every iteration → **O(n²) total**.

Building a `list` and joining at the end is **O(n + m)**. Always use the list-buffer-then-join pattern for any string building loop.

### Trace on `"abcd"`, `"pq"`

| i | j | out |
|---|---|---|
| 0 | 0 | ['a','p'] |
| 1 | 1 | ['a','p','b','q'] |
| 2 | 2 | (j >= len(word2)) exit loop |
| — | — | append word1[2:] = "cd" → ['a','p','b','q','cd'] |
| — | — | append word2[2:] = "" → unchanged |

Final: `"apbqcd"` ✓

### Complexity

- **Time:** O(n + m)
- **Space:** O(n + m) for the output

---

## Even shorter — `itertools.zip_longest`

```python
from itertools import zip_longest

class Solution:
    def mergeAlternately(self, word1, word2):
        return ''.join(a + b for a, b in zip_longest(word1, word2, fillvalue=''))
```

`zip_longest` pairs characters and fills with empty strings when one runs out. Elegant but reaches for a less-common builtin — fine to mention in an interview but **lead with the two-pointer version** to demonstrate the underlying logic.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Using `+=` to build the string | O(n²) total | List buffer + `.join()` |
| Stopping at `min(len)` and forgetting tails | Drops the longer string's overflow | Append `word1[i:]` and `word2[j:]` after the loop |
| Special-casing "which one is longer" | Unnecessary complication | Unconditional tail-append; empty slice is a no-op |
| Indexing past the end inside the loop | IndexError | Loop condition `i < len(word1) and j < len(word2)` |

---

## Interview Out-Loud

> "Two pointers walking both strings. Each round: take word1[i], then word2[j], advance both. When one runs out, the loop exits.
>
> After the loop, append both tails — word1[i:] and word2[j:]. Python slicing is empty when the index is past the end, so I don't need to check which one ran out.
>
> Build via a list and `.join()` at the end — string += is O(n²) in Python.
>
> O(n + m) time and space."

---

**Chain position:** Two-pointer string-merge warmup. Same shape in: Merge Two Sorted Lists, Merge Two Sorted Arrays.
