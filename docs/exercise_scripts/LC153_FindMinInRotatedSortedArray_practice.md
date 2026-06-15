# LC 153 — Find Minimum in Rotated Sorted Array · Practice Script

---

## Problem

> A sorted array (ascending, unique values) is rotated some number of times. Find the **minimum** element.
> You must write an algorithm with **O(log n) runtime**.

**Constraints:**
- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- All integers are **unique**.

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Are all values unique?"** — Yes, and it matters: duplicates break the comparison logic (that's LC 154, a different problem).
- **"Can the array be not rotated at all?"** — Yes — rotating n times gives the original. My code handles a fully sorted range with no special case: `nums[mid] < nums[right]` always holds, so it converges to index 0.
- **"Do you want the minimum value or its index?"** — The value. (The index would be the rotation count — a likely follow-up.)
- **"Is O(n) acceptable, or do you need O(log n)?"** — Spec demands O(log n), so `min(nums)` is only my stated baseline.

---

## NOT RECOMMENDED — Linear Scan (O(n))

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        return min(nums)
```

- **Time:** O(n) — touches every element.
- Correct, but ignores the "sorted-then-rotated" structure entirely. Spec demands O(log n).

State verbally:
> *"Brute force is just `min(nums)` — O(n). Spec requires O(log n), so I'll binary search comparing nums[mid] to nums[right] to detect which side of mid the rotation pivot sits on."*

---

## RECOMMENDED — Binary Search Variant (O(log n))

```python
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            # mid is bigger than the tail → the pivot (min) is strictly to the right
            if nums[mid] > nums[right]:
                left = mid + 1
            # mid is in the sorted tail → min is at mid or to its left (keep mid)
            else:
                right = mid
        return nums[left]
```

### The key insight

Compare `nums[mid]` to `nums[right]` — the **right end is a stable reference** relative to the rotation pivot:

- **`nums[mid] > nums[right]`** → mid is still in the higher (pre-pivot) run, so the minimum must be **strictly after** mid. Search RIGHT: `left = mid + 1`.
- **`nums[mid] < nums[right]`** → mid is already in the sorted tail that contains the min, so the min is at mid or to its left. Search LEFT: `right = mid` (keep mid — it could BE the min).

This needs no special case for an un-rotated array: if `nums` is already sorted, `nums[mid] < nums[right]` always holds, so `right` walks down to 0 and we return `nums[0]`. That's why it's simpler than comparing against `nums[left]`, which can't distinguish "already sorted" from "rotation on the right" without an extra check.

### Why `right = mid` (not `mid - 1`)

When mid is in the sorted tail, `nums[mid]` could BE the min. Excluding it with `right = mid - 1` would skip past the answer.

### Trace on `[4, 5, 6, 7, 0, 1, 2]`

| left | right | mid | nums[mid] | nums[right] | comparison | action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | 2 | 7 > 2 → pivot is right | left = 4 |
| 4 | 6 | 5 | 1 | 2 | 1 < 2 → mid in sorted tail | right = 5 |
| 4 | 5 | 4 | 0 | 1 | 0 < 1 → mid in sorted tail | right = 4 |

`left == right == 4` → exit, return `nums[4]` = **0** ✓

### Complexity

- **Time:** O(log n)
- **Space:** O(1)

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Comparing `nums[mid]` to `nums[left]` instead of `nums[right]` | Can't distinguish "already sorted" from "rotation on the right" — forces an awkward extra early-return check | Compare to `nums[right]`: it's a stable reference relative to the pivot, so two clean branches suffice |
| `right = mid - 1` when min could BE mid | Skips the answer | `right = mid` |
| `while left <= right` | Off-by-one — never exits when left == right | `while left < right` strictly |
| Returning `nums[mid]` from inside the loop | mid moves before convergence | Return `nums[left]` after the loop |
| Using `>=` in `nums[mid] > nums[right]` | With unique values it's harmless, but `>=` would wrongly push right past an equal tail in the duplicate variant | Keep strict `>`; handle duplicates separately (LC 154) |

---

## Interview Out-Loud

> "I'll binary search, comparing nums[mid] to nums[right] — the right end is a stable reference relative to the rotation pivot.
>
> If nums[mid] > nums[right], mid is still in the higher run before the pivot, so the minimum must be strictly to the right — left = mid + 1.
>
> Otherwise nums[mid] < nums[right], so mid is already in the sorted tail that holds the min — the min is at mid or to its left, so right = mid. I keep mid in scope because it could BE the minimum.
>
> No special case is needed for an un-rotated array: the else branch just walks right down to index 0.
>
> Loop while left < right. When they meet, that's the min — return nums[left].
>
> O(log n) time, O(1) space."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect a twist after the base solution works.

- **"What if duplicates are allowed?"** → LC 154 idea: when `nums[mid] == nums[right]` you can't tell which half holds the pivot, so shrink with `right -= 1`. Worst case degrades to O(n).
- **"Now search for a target in the rotated array."** → That's LC 33 — same "which half is sorted" test, then check if the target lies inside the sorted half. See its practice script.
- **"How many times was the array rotated?"** → It's just the index of the minimum — return `left` instead of `nums[left]`.
- **"Find the maximum instead."** → It sits immediately before the minimum: index `min_idx - 1`, wrapping with modulo for the unrotated case.

---

**Chain position:** Rotated-array binary search. Extends to: Search in Rotated Sorted Array (LC 33).
