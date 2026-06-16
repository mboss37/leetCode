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

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Are the intervals already sorted by start?"** — No, arbitrary order. Sorting first is the whole trick — it makes overlaps adjacent.
- **"Do TOUCHING intervals merge? [1,4] and [4,5]?"** — Yes, they merge to [1,5]. That's why the disjoint test is strict `>`, not `>=`.
- **"Can one interval fully contain another?"** — Yes. That's why the merged end takes `max(last.end, current.end)`, never just current's end.
- **"Can start equal end — point intervals like [5,5]?"** — Yes, constraints allow it; the same code handles them.
- **"May I reorder the input? Does output order matter?"** — I use `sorted()` so the caller's array is left untouched; output comes out sorted by start. (In-place `.sort()` also works if mutation is acceptable.)

---

## NOT RECOMMENDED — Pairwise Merge (O(n³))

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        result = sorted(intervals)          # sorted → a always starts at/before b
        changed = True
        while changed:
            changed = False
            for i in range(len(result)):
                for j in range(i + 1, len(result)):
                    a, b = result[i], result[j]
                    if b[0] <= a[1]:                    # overlap (a[0] <= b[0] guaranteed by sort)
                        result[i] = [a[0], max(a[1], b[1])]
                        result.pop(j)
                        changed = True
                        break
                if changed:
                    break
        return result
```

- **Time:** O(n³) worst case — repeatedly scan pairs and merge until stable.
- For n = 10⁴: ~10¹² ops → TLE.

> Sorting first means `result[i]` always starts at or before `result[j]` (since `i < j`), so the overlap test collapses from the two-sided `a[0] <= b[1] and b[0] <= a[1]` down to just `b[0] <= a[1]`.

State verbally:
> *"Brute force keeps rescanning pairs and merging on the fly until no more merges happen — O(n³). The fix isn't a better merge check, it's the sweep: once sorted, overlapping intervals are adjacent, so a single linear pass replaces the repeated rescans — O(n log n)."*

---

## RECOMMENDED — Intervals (sort + merge, O(n log n))

```python
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        merged = []
        for current in sorted(intervals):
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
| Forgetting to sort | Adjacent overlaps aren't adjacent in input | `sorted(intervals)` (or `intervals.sort()`) |
| Using `current[0] >= merged[-1][1]` | Touching intervals NOT merged ([1,4] and [4,5] stay separate) | Use `>` strictly; `≤` overlap rule |
| `merged[-1][1] = current[1]` instead of max | Shrinks last.end when current is nested | `max(merged[-1][1], current[1])` |
| Building result with tuples instead of lists | LC accepts both; tuples are immutable so can't extend | Use lists |

---

## Interview Out-Loud

> "Sort intervals by start time so overlapping intervals become adjacent. Sweep once: if the current interval starts AFTER the last merged ends, append it as new. Otherwise extend the last merged's end to max(last.end, current.end). Time O(n log n) — sort dominates. Space O(n)."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect one of these next:

- **"INSERT one new interval into an already-merged sorted list."** → LC 57 Insert Interval. Three phases: copy intervals ending before it, merge all that overlap, copy the rest. O(n), no re-sort.
- **"How many meeting rooms do these intervals need?"** → LC 253. Sort starts and ends separately and sweep, or use a min-heap of end times. The answer is max simultaneous overlaps.
- **"Remove the fewest intervals so the rest don't overlap."** → LC 435. Greedy: sort by END, keep each interval that starts at or after the last kept end.
- **"Intervals arrive one at a time as a stream."** → Keep the merged list sorted and run the LC 57 insert per arrival — O(n) each, or an interval tree if pushed.

---

**Chain position:** Intervals pattern (sort by start, then merge). Same shape applies to: Insert Interval, Meeting Rooms, Non-overlapping Intervals.
