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

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Are all values unique, or can there be duplicates?"** — Unique here. Duplicates break the "which half is sorted" test and degrade to O(n) worst case (that's LC 81).
- **"Can the array be not rotated at all?"** — Yes, rotation by 0 is allowed. The same code handles it — the left half just always tests as sorted.
- **"Return the index or the value? What if target is missing?"** — Index; -1 if missing.
- **"Is the array ascending before rotation?"** — Yes. Descending would flip every comparison.
- **"Is O(n) acceptable or do you need O(log n)?"** — Spec demands O(log n), so a linear scan is off the table.

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

## Likely Follow-ups

The interview is one question that grows in parts — expect one of these next:

- **"Find the MINIMUM element instead of a target."** → That is literally LC 153 Find Minimum in Rotated Sorted Array — there's a practice script for it in this repo. Binary search toward the unsorted side; the min is the pivot.
- **"What if duplicates are allowed?"** → LC 81. When `nums[left] == nums[mid] == nums[right]` you can't tell which half is sorted — shrink both ends by one. Worst case becomes O(n).
- **"Find how many times the array was rotated."** → Same as finding the min: its index IS the rotation count.
- **"Target appears multiple times — return the first occurrence."** → Only meaningful with duplicates; after finding any match, binary-search left for the boundary (LC 34 style).

---

**Chain position:** Binary search variants on rotated arrays. Related: Find Minimum in Rotated Sorted Array (LC 153).
