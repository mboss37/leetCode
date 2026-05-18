# LC 153 — Find Minimum in Rotated Sorted Array · Practice Script

**Code:** [code/findMinRotated/](../../code/findMinRotated/)

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

## RECOMMENDED — Binary Search Variant (O(log n))

```python
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1     # pivot is in the right half
            else:
                right = mid        # min is in the left half (could be mid)
        return nums[left]
```

### The key insight

In a rotated sorted array, **one half is always sorted**. Compare `nums[mid]` to `nums[right]`:

- **`nums[mid] > nums[right]`** → the right half contains the rotation pivot (and therefore the min). Search RIGHT: `left = mid + 1`.
- **`nums[mid] ≤ nums[right]`** → the right half is sorted, so the min is in the left half (or is mid itself). Search LEFT: `right = mid` (don't exclude mid).

### Why compare to `right`, not `left`

Compare to `left` and you can't always tell which half is sorted — `nums[mid] ≥ nums[left]` happens in both rotated and non-rotated cases. Comparing to `right` uniquely identifies which side contains the pivot.

### Why `right = mid` (not `mid - 1`)

When `nums[mid] ≤ nums[right]`, `nums[mid]` could BE the min. Excluding it with `right = mid - 1` would skip past the answer.

### Trace on `[4, 5, 6, 7, 0, 1, 2]`

| left | right | mid | nums[mid] | nums[right] | compare | action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | 2 | 7 > 2 | left = 4 |
| 4 | 6 | 5 | 1 | 2 | 1 < 2 | right = 5 |
| 4 | 5 | 4 | 0 | 1 | 0 < 1 | right = 4 |
| 4 | 4 | — exit — | | | | return nums[4] = 0 |

Returns **0** ✓

### Complexity

- **Time:** O(log n)
- **Space:** O(1)

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Comparing to `left` instead of `right` | Can't reliably identify the rotated half | Compare to `right` |
| `right = mid - 1` when min could BE mid | Skips the answer | `right = mid` |
| `while left <= right` | Off-by-one — never exits if left == right | `while left < right` strictly |
| Returning `nums[mid]` from inside the loop | mid moves before convergence | Return `nums[left]` after the loop |

---

## Interview Out-Loud

> "One half of a rotated sorted array is always sorted. I'll use binary search comparing nums[mid] to nums[right]. If mid > right, the pivot is in the right half — go right. Otherwise the right half is sorted, so the min is in the left half or is mid itself — go left, keeping mid in scope.
>
> Loop while left < right. When they meet, that's the min.
>
> O(log n) time, O(1) space."

---

**Chain position:** Rotated-array binary search. Extends to: Search in Rotated Sorted Array (LC 33).
