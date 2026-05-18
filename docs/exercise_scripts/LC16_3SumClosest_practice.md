# LC 16 — 3Sum Closest · Practice Script

---

## Problem

> Given an integer array `nums` of length `n` and an integer `target`, find three integers in `nums` such that the sum is **closest** to `target`. Return the **sum** of the three integers.
>
> You may assume that each input would have **exactly one solution**.

**Constraints:**
- `3 <= nums.length <= 500`
- `-1000 <= nums[i] <= 1000`
- `-10⁴ <= target <= 10⁴`

**Key difference from LC 15:** the output is a **single integer** (the closest sum). No list, no dedup.

---

## 1. Brute Force (O(n³))

```python
from typing import List

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        n = len(nums)
        closest_sum = nums[0] + nums[1] + nums[2]    # baseline

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    current_sum = nums[i] + nums[j] + nums[k]
                    if abs(current_sum - target) < abs(closest_sum - target):
                        closest_sum = current_sum
        return closest_sum
```

- **Time:** O(n³). At n=500: ~21M operations.
- **Space:** O(1).
- **State out loud:** "Three nested loops, O(n³). For n=500, borderline acceptable. Optimal is O(n²) — sort plus two-pointer."

---

## 2. Optimal — Sort + Two-Pointer (O(n²))

```python
from typing import List

class Solution:
    def threeSumClosest(self, numbers: List[int], target: int) -> int:
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        closest_sum = sorted_nums[0] + sorted_nums[1] + sorted_nums[2]

        for i in range(n - 2):
            left = i + 1
            right = n - 1

            while left < right:
                current_sum = sorted_nums[i] + sorted_nums[left] + sorted_nums[right]

                if abs(current_sum - target) < abs(closest_sum - target):
                    closest_sum = current_sum

                if current_sum < target:
                    left += 1
                elif current_sum > target:
                    right -= 1
                else:
                    return target  # distance 0 — unbeatable

        return closest_sum
```

### Why this works

1. **Sort.** Same as LC 167 / LC 15 — moving L right raises the sum, moving R left lowers it. No backtracking.
2. **Outer anchor `i`** fixes the first element; inner two-pointer finds the best pair of remaining numbers.
3. **Distance check every iteration.** Unlike LC 15 (act only on `sum == 0`), here EVERY sum is a candidate for "closest." So we update `closest_sum` whenever the current distance beats the best distance.
4. **Three-branch direction logic:**
   - `sum < target` → L moves right (bigger).
   - `sum > target` → R moves left (smaller).
   - `sum == target` → distance is 0. **Return immediately** — no other triplet can beat that.
5. **No dedup needed.** Output is a single number; duplicate sums don't corrupt anything. Skip checks are unnecessary.

### Complexity

- **Time:** O(n²) — outer O(n), inner two-pointer O(n).
- **Space:** O(1) auxiliary (excluding the sorted copy).

---

## 3. Brute Force vs Two-Pointer

| Aspect              | Brute Force (O(n³))         | Two-Pointer (O(n²))         | Winner       |
|---------------------|------------------------------|------------------------------|--------------|
| Time                | O(n³)                        | O(n²)                        | Two-Pointer  |
| Space               | O(1)                         | O(1) auxiliary               | Tie          |
| Sorts the array     | No                           | Yes                          | —            |
| Lines of code       | ~10                          | ~15                          | Brute Force  |
| n=500 ops           | ~21M                         | ~250K                        | Two-Pointer  |

---

## 4. Test Cases

| nums                          | target | Expected | Notes |
|-------------------------------|--------|----------|-------|
| `[-1, 2, 1, -4]`              | 1      | 2        | Canonical example |
| `[0, 0, 0]`                   | 1      | 0        | Only one triplet possible |
| `[1, 1, 1, 0]`                | -100   | 2        | All sums far from target |
| `[-1, 0, 1, 2, -1, -4]`       | 5      | 3        | Multiple candidates |
| `[-3, -2, -5, 3, -4]`         | -1     | -2       | Negative target & answer |

---

## 5. Interview Out-Loud Explanation

> "Brute force is three nested loops, O(n³). At n=500 it's about 21M operations — borderline. I'll use sort plus two-pointer for O(n²).
>
> Sort the array first. This unlocks two-pointer reasoning — moving left right raises the sum, moving right left lowers it.
>
> Initialize `closest_sum` to the sum of the first three elements as a baseline.
>
> Outer loop walks an anchor `i`. For each anchor, run a two-pointer scan with `left = i + 1` and `right = n - 1`. On every iteration, compute the three-way sum. If its absolute distance from target is smaller than the best so far, update `closest_sum`.
>
> Three-branch direction: if sum less than target, move left right; if sum greater than target, move right left; if exactly equal, return target immediately — distance zero is unbeatable.
>
> No dedup logic — the output is a single number, so duplicate sums don't corrupt the answer.
>
> Total: O(n²) time, O(1) auxiliary space."

---

## 6. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| `left = 0` | L can equal i → same element used twice | `left = i + 1` |
| No `while` loop | Inner runs once per anchor | Wrap in `while left < right:` |
| `abs(current) < closest_sum` | Comparing distance to a sum | `abs(current - target) < abs(closest - target)` |
| Skip checks copied from LC 15 | Unnecessary complexity | Drop them — no dedup needed here |
| Initialize from `numbers[:3]` (unsorted) | Just a taste issue | Either works; use `sorted_nums[:3]` for consistency |

---

**Chain position:** LC 1 → LC 167 → LC 15 → **LC 16** → (later: LC 18 / 4Sum).

3Sum Closest is the "simpler cousin" of 3Sum — same skeleton, fewer concerns.
