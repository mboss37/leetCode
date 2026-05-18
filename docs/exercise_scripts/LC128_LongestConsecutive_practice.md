# LC 128 — Longest Consecutive Sequence · Practice Script

**Code:** [code/longestConsecutive/](../../code/longestConsecutive/)

**Chain:** Contains Duplicate (set existence) → **Longest Consecutive Sequence** (set + anchor)

---

## Problem

> Given an unsorted array of integers `nums`, return the **length** of the **longest consecutive elements sequence**.
>
> You must write an algorithm that runs in **O(n)** time.

**Constraints:**
- `0 <= nums.length <= 10⁵`
- `-10⁹ <= nums[i] <= 10⁹`

**Critical:** the **O(n) requirement explicitly rules out sorting** (O(n log n)).

---

## 1. NOT RECOMMENDED — Sort + Sweep (O(n log n))

```python
from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        sorted_arr = sorted(set(nums))   # dedupe + sort
        best = 1
        current = 1

        for i in range(1, len(sorted_arr)):
            if sorted_arr[i] - sorted_arr[i - 1] == 1:
                current += 1
                best = max(best, current)
            else:
                current = 1   # reset on gap break
        return best
```

- **Time: O(n log n)** — sort dominates
- **Space: O(n)** — `sorted()` creates a new list
- **Rejected by spec.** Spec demands O(n).

State it verbally:
> *"Naive is sort + sweep, O(n log n). Spec wants O(n), so I'll use a set + anchor check instead."*

### Two bugs to avoid in the sort + sweep version

1. **Counting TOTAL gaps-of-1 instead of LONGEST RUN.** You must track `current` and `best` separately and RESET `current` on each gap break.
2. **Duplicates create gap=0.** Easiest fix: `sorted(set(nums))` to dedupe upfront so all gaps are either 1 or > 1.

---

## 2. RECOMMENDED — Set + Anchor (O(n))

```python
from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        s = set(nums)
        best = 0

        for num in s:
            # Anchor check — only start counting from the SMALLEST of a chain.
            if (num - 1) not in s:
                current = num
                length = 1
                while (current + 1) in s:
                    current += 1
                    length += 1
                best = max(best, length)

        return best
```

### The key insight — the "anchor check"

For each number, ask: *"Is `num - 1` in the set?"*

- **YES** → `num` is mid-chain. SKIP it — a smaller anchor will count this chain.
- **NO** → `num` is the **anchor** (smallest element of its chain). Walk forward and count.

Without this check, every element would walk its full chain → O(n²). With it, **only anchors walk** → O(n).

### Why this is O(n) despite the nested `while`

Looks like O(n²) at first glance: outer loop over n elements, inner while loop walks a chain. But:

- The inner while only runs for **anchors**. Non-anchors fail the `if (num - 1) not in s` check in O(1).
- **Each element belongs to exactly ONE chain** and is walked exactly ONCE (when its anchor visits it).
- Total walk-work across all anchors ≤ n.
- Outer loop = n. Walk-work = n. Total = **O(n)**.

### Trace on `[2, 20, 4, 10, 3, 4, 5]`

`s = {2, 3, 4, 5, 10, 20}` (duplicate 4 collapses).

| num | `num - 1` in s? | Anchor? | Walk | length | best |
|---|---|---|---|---|---|
| 2 | 1 not in s | **YES** | 2 → 3 → 4 → 5 → stops | 4 | **4** |
| 3 | 2 in s | no | skip | — | 4 |
| 4 | 3 in s | no | skip | — | 4 |
| 5 | 4 in s | no | skip | — | 4 |
| 10 | 9 not in s | **YES** | 10 → stops | 1 | 4 |
| 20 | 19 not in s | **YES** | 20 → stops | 1 | 4 |

Return `best = 4` ✓

### Complexity

- **Time: O(n)** — each element visited a constant number of times
- **Space: O(n)** — the set

---

## 3. Comparison

| Approach | Time | Space | Accepted by spec? |
|---|---|---|---|
| Sort + sweep | O(n log n) | O(n) | ❌ NO (spec demands O(n)) |
| **Set + anchor** | **O(n)** | O(n) | **✓ YES** |

---

## 4. How to Practice

### Step 1: Read out loud

> "Naive is sort + sweep, O(n log n). Spec demands O(n) so that's rejected. I'll use a set + anchor check.
>
> Put everything in a set for O(1) membership lookup. For each number, check if `num - 1` is in the set. If yes, this number is mid-chain — skip. If no, this number is the START of a chain (the anchor). Walk forward, incrementing the count while the next number is in the set.
>
> Why is it O(n) despite the nested while loop? Because each element is visited at most twice — once by the outer loop, and possibly once by an anchor's walk. The anchor check guarantees we don't re-walk the same chain from different starting points.
>
> Time: O(n). Space: O(n) for the set."

### Step 2: Key Points

- **Always do the anchor check** (`if (num - 1) not in s`) — without it, the algorithm degrades to O(n²).
- **Iterate over the set, not the input list** — duplicates would just trigger redundant skips.
- **`best = 0`** initialization handles empty input correctly.
- **The walk is `while (current + 1) in s`** — check BEFORE advancing.

### Step 3: Test Cases

| nums | Expected | Notes |
|---|---|---|
| `[100, 4, 200, 1, 3, 2]` | 4 | Canonical |
| `[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]` | 9 | Two duplicates, one long chain |
| `[]` | 0 | Empty |
| `[1, 2, 0, 1]` | 3 | Has duplicate, chain [0,1,2] |
| `[1]` | 1 | Single element |
| `[1, 2, 3, 10, 11]` | 3 | Two disjoint chains — pick the longer |
| `[1, 0, -1]` | 3 | Negatives handled by hashing |

---

## 5. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| No anchor check, walk every element's chain | O(n²) — re-walks the same chain from each starting point | `if (num - 1) not in s` GUARD before walking |
| `for num in nums` instead of `for num in s` | Duplicates trigger redundant skips | Iterate over the set |
| Sort + sweep approach | Spec demands O(n); sort is O(n log n) | Use set + anchor |
| Counting TOTAL gaps==1 in sort+sweep | Combines disconnected chains into one count | Track `current` vs `best`, reset on gap |
| Forgetting to handle empty input | `best = 0` doesn't update → returns 0 (which is correct!) | Lucky default, but state it explicitly |

---

## 6. Interview Out-Loud Explanation

> "I'll use a set for O(1) membership lookup. Iterate each unique value. For each value, the trick is: only START counting from the SMALLEST of a chain. If `num - 1` is in the set, this value is mid-chain — a smaller anchor will count it. Skip. Otherwise, walk forward from this anchor, counting how far the chain extends.
>
> Why is this O(n)? Each element is part of exactly ONE chain and is walked exactly ONCE — when its anchor visits it. Non-anchors get an O(1) check-and-skip. Total work is linear.
>
> Time: O(n). Space: O(n) for the set."

---

**Chain position:** Longest Consecutive Sequence is the canonical **"set + anchor"** pattern. The "only-start-at-the-floor-of-a-chain" idea also appears in:
- **Number of Islands** (Phase C) — only start a DFS at unvisited land cells (similar anchor concept)
- **Some interval problems** — only process the leftmost interval of a group

The reflex: when you see "find longest run / longest chain / longest island in unsorted input," reach for set + anchor.
