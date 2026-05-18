# LC 49 — Group Anagrams · Practice Script

**Chain:** Valid Anagram → **Group Anagrams** → variants where you group by some other canonical key

---

## Problem

> Given an array of strings `strs`, **group the anagrams together**. You can return the answer in any order.

**Constraints:**
- `1 <= strs.length <= 10⁴`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters only.

**Output order:** doesn't matter — groups can appear in any order, and strings within groups can appear in any order.

---

## 1. Brute Force (verbal baseline only — DON'T WRITE)

Pairwise comparison: for each unvisited string, scan every other unvisited string and group anagrams together using `Counter(a) == Counter(b)`.

- **Time:** O(n² · k) — outer n, inner n, anagram check is O(k).
- **Space:** O(n · k) — output + visited array.
- **Why rejected:** awkward double loop, no use of the hash-map "group by key" pattern. Recommended solution is both shorter AND faster.

State it verbally only:
> *"Naive is pairwise comparison — O(n² · k). I'll use a hash map keyed by sorted letters for O(n · k log k)."*

---

## 2. RECOMMENDED — Hash map keyed by sorted letters (~3 lines)

```python
from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            key = ''.join(sorted(s))
            groups[key].append(s)
        return list(groups.values())
```

### Why this works

**Anagrams share an invariant: the same multiset of letters.** Sort the letters of each string to produce a **canonical key**. Strings that are anagrams of each other produce identical keys.

- `''.join(sorted(s))` → sort the chars, then glue them back into a string.
- `defaultdict(list)` → on first sight of a key, auto-creates an empty list. Skips the `if key not in groups: groups[key] = []` boilerplate.
- `groups[key].append(s)` → drop the string into its anagram group.

### Trace on `["eat", "tea", "tan", "ate", "nat", "bat"]`

| s | sorted(s) | key | groups after |
|---|---|---|---|
| "eat" | ['a','e','t'] | "aet" | `{"aet": ["eat"]}` |
| "tea" | ['a','e','t'] | "aet" | `{"aet": ["eat","tea"]}` |
| "tan" | ['a','n','t'] | "ant" | `{"aet": [...], "ant": ["tan"]}` |
| "ate" | ['a','e','t'] | "aet" | `{"aet": ["eat","tea","ate"], ...}` |
| "nat" | ['a','n','t'] | "ant" | `{"aet": [...], "ant": ["tan","nat"]}` |
| "bat" | ['a','b','t'] | "abt" | `{..., "abt": ["bat"]}` |

Return `list(groups.values())` → `[["eat","tea","ate"], ["tan","nat"], ["bat"]]` ✓

### Complexity

- **Time:** O(n · k log k) — n strings, each sorted in O(k log k).
- **Space:** O(n · k) — every string is stored once across the groups + the sorted keys.

---

## 3. Optional — Count-Tuple key (asymptotically faster)

```python
from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            counts = [0] * 26
            for c in s:
                counts[ord(c) - ord('a')] += 1
            groups[tuple(counts)].append(s)
        return list(groups.values())
```

Skips the sort. Each string is processed in O(k) — no log factor.

- **Time:** O(n · k) — strictly better than sort version.
- **Space:** O(n · k) — same as sort version.
- **Trade-off:** more code, and **assumes lowercase a-z only** (the 26-slot array hardcodes the alphabet).

### Interview phrasing

> *"If we need to squeeze out the log factor, swap the sorted-string key for a 26-element count tuple. Each string is then O(k) to process. Tied to lowercase a-z, but the input spec allows that here."*

---

## 4. Comparison

| Approach | Time | Space | Lines | When to use |
|---|---|---|---|---|
| Brute force pairwise | O(n² · k) | O(n · k) | ~10 | NEVER write — verbal baseline only |
| **Sorted-string key** | O(n · k log k) | O(n · k) | **~3** | **DEFAULT** — Pythonic, general |
| Count-tuple key | **O(n · k)** | O(n · k) | ~7 | Asked to optimize / fixed alphabet |

---

## 5. How to Practice

### Step 1: Read out loud

> "Anagrams share an invariant — the same letters. If I make a canonical key from each string (sorted letters), all anagrams produce identical keys. Use `defaultdict(list)` to group: for each string, compute the key, append to the list under that key.
>
> Time: O(n · k log k) — n strings, each sorted in O(k log k). Space: O(n · k) — every string lives once in the output.
>
> If the interviewer asks for faster, I can swap the sorted-string key for a 26-element count tuple — that drops the log factor to O(n · k)."

### Step 2: Key Points

- **`defaultdict(list)`** auto-creates the bucket on first sight — skips the `if key not in groups` dance.
- **`''.join(sorted(s))`** is the standard "canonical anagram key" idiom.
- **`list(groups.values())`** returns the groups in insertion order (Python 3.7+ guarantees dict order).
- **Tuple, not list, for the count-tuple key** — lists aren't hashable.

### Step 3: Test Cases

| strs | Expected (any order) | Notes |
|---|---|---|
| `["eat","tea","tan","ate","nat","bat"]` | `[["eat","tea","ate"], ["tan","nat"], ["bat"]]` | Canonical |
| `[""]` | `[[""]]` | Empty string still groups |
| `["a"]` | `[["a"]]` | Single char |
| `["abc","bca","cab","xyz","zyx","yxz","no"]` | 3 groups | Multiple full-anagram clusters |
| `["abc","def"]` | `[["abc"],["def"]]` | No anagrams — each in its own group |

### Step 4: Full Testing Code

```python
from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            key = ''.join(sorted(s))
            groups[key].append(s)
        return list(groups.values())


# ============= TEST CASES =============
solution = Solution()
print(solution.groupAnagrams(["eat","tea","tan","ate","nat","bat"]))
print(solution.groupAnagrams([""]))
print(solution.groupAnagrams(["a"]))
print(solution.groupAnagrams(["abc","bca","cab","xyz","zyx","yxz","no"]))
```

---

## 6. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Plain `dict` instead of `defaultdict(list)` | Need `if key not in groups: groups[key] = []` boilerplate every iteration | Use `defaultdict(list)` — auto-creates buckets |
| Using a `list` as a dict key | TypeError — lists are mutable, not hashable | Convert to `tuple` for the count-array version |
| Forgetting `''.join(...)` after `sorted(s)` | `sorted(s)` returns a LIST of chars, not a string | `''.join(sorted(s))` gives a string key |
| Returning `groups` instead of `groups.values()` | Returns the dict, not the list of groups | `return list(groups.values())` |
| Writing the brute force pairwise version | Wastes time, more bugs, slower | State verbally, write the hash-map version |

---

## 7. Interview Out-Loud Explanation

> "Anagrams share a canonical key — the same letters in the same order if you sort. I'll group strings by that key.
>
> Use `defaultdict(list)`. For each string, sort the letters to make the key, then append the string under that key. At the end, return the list of all groups.
>
> Time: O(n · k log k) — n strings, each sorted in O(k log k). Space: O(n · k) for storing the input across the groups.
>
> If you want me to drop the log factor, I can swap the sort for a 26-element count tuple — O(n · k) time. Works because the input is lowercase a-z only."

---

**Chain position:** Group Anagrams is the **"group by derived key"** pattern. Same idea extends to:
- **Sort Characters By Frequency** — key by frequency
- **Top K Frequent Words** — combination with Counter
- **Find All Anagrams in a String** (different problem: sliding window with Counter equality)

The `defaultdict(list).append()` reflex is what you internalize here. Reach for it any time you see "group X by some derived property."
