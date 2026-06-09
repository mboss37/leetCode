# LC 1768 — Merge Strings Alternately · Practice Script

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

## Clarifying Questions (ask 2-3 before you code)

The interviewer wants requirements pinned down before you type — pick the ones that genuinely change your code:

- **"What happens when the strings have unequal lengths?"** — The leftover of the longer one is appended at the end. This IS the core of the problem.
- **"Which string starts the alternation?"** — `word1`. Getting the order backwards is the cheapest possible bug.
- **"Can either string be empty?"** — Constraints say length ≥ 1, but the tail-append version handles empty for free — worth saying.
- **"Return a new string or modify in place?"** — Python strings are immutable, so always a new string.
- **"One character at a time, or word by word?"** — One character at a time. Confirm before coding.

---

## No meaningful brute force

The operation is inherently O(n + m) — every character must be touched once. The two-pointer version below is the simplest expression of that floor. No slower comparative is worth writing.

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

## ALTERNATIVE — `itertools.zip_longest` (one-liner)

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

## Likely Follow-ups

This warmup grows into parts — have the next steps ready.

- **"Why not build the result with `+=`?"** → Strings are immutable; each `+=` copies the whole string, O(n²) total. List buffer + `join` is O(n + m).
- **"Can you do it without manual indices?"** → Yes — `zip_longest` with `fillvalue=''` (the Alternative section above). Lead with two pointers, mention this.
- **"Now merge k strings alternately."** → Same loop over a list of pointers, or `zip_longest(*words, fillvalue='')`.
- **"Same idea on linked lists?"** → That is Merge Two Sorted Lists — same two-pointer-plus-tail shape, see the chain note below.

---

**Chain position:** Two-pointer string-merge warmup. Same shape in: Merge Two Sorted Lists, Merge Two Sorted Arrays.
