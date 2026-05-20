# LC 33 — Search in Rotated Sorted Array · Practice Script

---

## Problem

> Sorted array (ascending, unique) rotated at some unknown pivot. Return the **index** of `target` if it exists, else `-1`.
> You must write an algorithm with **O(log n) runtime**.

**Constraints:**
- `1 <= nums.length <= 5000`
- `-10⁴ <= nums[i], target <= 10⁴`
- All values unique.

---

## NOT RECOMMENDED — Linear Scan (O(n))

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i, x in enumerate(nums):
            if x == target:
                return i
        return -1
```

- **Time:** O(n).
- Correct but ignores the sorted structure. Spec requires O(log n).

State verbally:
> *"Brute force is walk the array — O(n). Spec demands O(log n), so I'll binary search; at each step one half is sorted, and I check if target lies in that sorted half's range to decide which side to recurse."*

---

## RECOMMENDED — Binary Search with Pivot Detection (O(log n))

```python
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            # Identify which half is sorted
            if nums[left] <= nums[mid]:
                # Left half is sorted
                if nums[left] <= target < nums[mid]:
                    right = mid - 1   # target in left half
                else:
                    left = mid + 1
            else:
                # Right half is sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1    # target in right half
                else:
                    right = mid - 1
        return -1
```

### The key idea

**One half is always sorted.** Determine which:

- `nums[left] ≤ nums[mid]` → left half `[left..mid]` is sorted.
- Else → right half `[mid..right]` is sorted.

Then check whether target falls within the **sorted half's range**:
- If yes → search the sorted half.
- If no → search the unsorted half (where the pivot lives).

Each step halves the search range → **O(log n)**.

### Trace on `[4, 5, 6, 7, 0, 1, 2]`, target = 0

| left | right | mid | nums[mid] | which half sorted? | target in sorted half? | action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | left [4,5,6,7] sorted | 0 ∉ [4, 7) → no | left = 4 |
| 4 | 6 | 5 | 1 | left [0,1] sorted (nums[4]=0 ≤ nums[5]=1) | 0 ∈ [0, 1) → yes | right = 4 |
| 4 | 4 | 4 | 0 | **match** → return 4 ✓ | | |

### Complexity

- **Time:** O(log n)
- **Space:** O(1)

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Using `<` instead of `<=` in `nums[left] <= nums[mid]` | When left == mid (range of 1), gets the wrong half | Use `<=` |
| Wrong bounds for "target in sorted half" | Misses target near the boundaries | `nums[left] <= target < nums[mid]` (strict on the side that's mid) |
| Forgetting the `==` check | Returns -1 even when mid IS the target | `if nums[mid] == target: return mid` first |
| `while left < right` instead of `<=` | Misses single-element check | Use `<=` for exact match |

---

## Interview Out-Loud

> "Standard binary search but the array is rotated, so I figure out which half is sorted at each step.
>
> If nums[left] ≤ nums[mid], the LEFT half is sorted. Check if target falls in [nums[left], nums[mid]) — if yes, search left, else search right.
>
> Otherwise the RIGHT half is sorted. Check if target falls in (nums[mid], nums[right]] — if yes, search right, else search left.
>
> Each step halves the range → O(log n). O(1) space."

---

**Chain position:** Binary search variants on rotated arrays. Related: Find Minimum in Rotated Sorted Array (LC 153).
