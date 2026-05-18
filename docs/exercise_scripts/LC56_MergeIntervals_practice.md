# LC 56 — Merge Intervals · Practice Script

---

## Problem

> Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, **merge all overlapping intervals** and return an array of the non-overlapping intervals covering all input.

**Constraints:**
- `1 <= intervals.length <= 10⁴`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10⁴`

**Overlap definition:** intervals overlap if one's start ≤ the other's end. Touching counts (e.g., `[1,4]` and `[4,5]` merge to `[1,5]`).

---

## NOT RECOMMENDED — Pairwise Merge (O(n³))

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        result = [list(iv) for iv in intervals]
        changed = True
        while changed:
            changed = False
            for i in range(len(result)):
                for j in range(i + 1, len(result)):
                    a, b = result[i], result[j]
                    if a[0] <= b[1] and b[0] <= a[1]:   # overlap
                        result[i] = [min(a[0], b[0]), max(a[1], b[1])]
                        result.pop(j)
                        changed = True
                        break
                if changed:
                    break
        return result
```

- **Time:** O(n³) worst case — repeatedly scan pairs and merge until stable.
- For n = 10⁴: ~10¹² ops → TLE.

State verbally:
> *"Brute force is keep scanning pairs and merging on the fly until no more merges happen. O(n³). I'll sort by start time so overlapping intervals become adjacent, then a single linear sweep handles it — O(n log n)."*

---

## RECOMMENDED — Sort + Sweep (O(n log n))

```python
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = []
        for current in intervals:
            if not merged or current[0] > merged[-1][1]:
                merged.append(current)
            else:
                merged[-1][1] = max(merged[-1][1], current[1])
        return merged
```

### How it works

**Sorting by start time makes overlapping intervals ADJACENT.** Once adjacent, a single linear sweep merges them:

- If `merged` is empty OR current.start > last.end → **disjoint**, append new entry.
- Else → **overlap**, extend `last.end = max(last.end, current.end)`.

### Why `max(last.end, current.end)`

Could be that `current` is fully **nested** inside `last` (e.g., `last=[1,10]`, `current=[2,3]`). In that case, `last.end` is already bigger and shouldn't shrink. Always take the MAX.

### Trace on `[[1,3], [2,6], [8,10], [15,18]]`

Sorted: `[[1,3], [2,6], [8,10], [15,18]]` (already sorted).

| current | merged before | merged after |
|---|---|---|
| [1,3] | [] | [[1,3]] (empty → append) |
| [2,6] | [[1,3]] | [[1,6]] (2 ≤ 3 → extend end to max(3,6)=6) |
| [8,10] | [[1,6]] | [[1,6],[8,10]] (8 > 6 → append) |
| [15,18] | [[1,6],[8,10]] | [[1,6],[8,10],[15,18]] (15 > 10 → append) |

### Complexity

- **Time:** O(n log n) — sort dominates
- **Space:** O(n) — output list

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting to sort | Adjacent overlaps aren't adjacent in input | `intervals.sort(key=lambda x: x[0])` |
| Using `current[0] >= merged[-1][1]` | Touching intervals NOT merged ([1,4] and [4,5] stay separate) | Use `>` strictly; `≤` overlap rule |
| `merged[-1][1] = current[1]` instead of max | Shrinks last.end when current is nested | `max(merged[-1][1], current[1])` |
| Building result with tuples instead of lists | LC accepts both; tuples are immutable so can't extend | Use lists |

---

## Interview Out-Loud

> "Sort intervals by start time so overlapping intervals become adjacent. Sweep once: if the current interval starts AFTER the last merged ends, append it as new. Otherwise extend the last merged's end to max(last.end, current.end). Time O(n log n) — sort dominates. Space O(n)."

---

**Chain position:** Sort + sweep pattern. Same shape applies to: Insert Interval, Meeting Rooms, Non-overlapping Intervals.
