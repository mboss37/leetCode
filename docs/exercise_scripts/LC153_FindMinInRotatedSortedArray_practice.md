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

## NOT RECOMMENDED — Linear Scan (O(n))

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        return min(nums)
```

- **Time:** O(n) — touches every element.
- Correct, but ignores the "sorted-then-rotated" structure entirely. Spec demands O(log n).

State verbally:
> *"Brute force is just `min(nums)` — O(n). Spec requires O(log n), so I'll binary search comparing nums[mid] to nums[right] to detect which half contains the rotation pivot."*

---

## RECOMMENDED — Binary Search Variant (O(log n))

```python
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            # Is the left half sorted?
            if nums[left] <= nums[mid]:
                # Is the current search slice [left..right] also sorted? (no drop at all here)
                if nums[mid] <= nums[right]:
                    return nums[left]
                # Only the left is sorted → the drop is on the right
                left = mid + 1
            else:
                # Left half is NOT sorted → the drop is on the left
                right = mid
        return nums[left]
```

### The key insight

In a rotated sorted array, **one half is always sorted**. Compare `nums[left]` to `nums[mid]` (same comparison as LC 33):

- **`nums[left] ≤ nums[mid]`** → left half `[left..mid]` is sorted. The min is either at `left` (if the whole range is sorted) or in the right half (if rotation is there).
- **`nums[left] > nums[mid]`** → left half contains the rotation pivot. The min is in `[left..mid]`. Search LEFT: `right = mid` (don't exclude mid).

### Why `right = mid` (not `mid - 1`)

When the rotation is in the left half, `nums[mid]` could BE the min. Excluding it with `right = mid - 1` would skip past the answer.

### Trace on `[4, 5, 6, 7, 0, 1, 2]`

| left | right | mid | nums[left] | nums[mid] | nums[right] | which half sorted? | action |
|---|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 4 | 7 | 2 | left sorted (4≤7) | mid 7 > right 2 → rotation right → left = 4 |
| 4 | 6 | 5 | 0 | 1 | 2 | left sorted (0≤1) | mid 1 ≤ right 2 → whole range sorted → return nums[4] = 0 |

Returns **0** ✓

### Complexity

- **Time:** O(log n)
- **Space:** O(1)

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting the `nums[mid] <= nums[right]` early-return | Loop never terminates on already-sorted ranges; or you miscompute which half has the rotation | Inner check after `nums[left] <= nums[mid]`: if `nums[mid] <= nums[right]`, range is sorted → return `nums[left]` |
| `right = mid - 1` when min could BE mid | Skips the answer | `right = mid` |
| `while left <= right` | Off-by-one — never exits if left == right | `while left < right` strictly |
| Returning `nums[mid]` from inside the loop | mid moves before convergence | Return `nums[left]` after the loop (or via the early-return) |

---

## Interview Out-Loud

> "One half of a rotated sorted array is always sorted. I'll use binary search comparing nums[left] to nums[mid] — same convention as LC 33.
>
> If left ≤ mid, the left half is sorted. Then I check if mid ≤ right too — if yes, the whole range is sorted and the min is at left. Otherwise the rotation is in the right half, so I narrow there.
>
> If left > mid, the rotation is in the left half — narrow there with right = mid (keeping mid in scope, since it could BE the min).
>
> Loop while left < right. When they meet, that's the min.
>
> O(log n) time, O(1) space."

---

**Chain position:** Rotated-array binary search. Extends to: Search in Rotated Sorted Array (LC 33).
