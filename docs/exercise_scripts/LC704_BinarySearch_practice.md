# LC 704 — Binary Search · Practice Script

---

## Problem

> Given a **sorted** (ascending) array of integers `nums` and an integer `target`, return the **index** of `target` in `nums`. If `target` doesn't exist, return `-1`.
>
> You must write an algorithm with **O(log n) runtime complexity**.

**Constraints:**
- `1 <= nums.length <= 10⁴`
- `-10⁴ < nums[i], target < 10⁴`
- All integers in `nums` are **unique**.
- `nums` is sorted in **ascending order**.

**Key fact:** the problem explicitly REQUIRES O(log n). Linear scan would solve it correctly but be rejected.

---

## 1. Linear Scan — NOT RECOMMENDED (O(n))

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i, value in enumerate(nums):
            if value == target:
                return i
        return -1
```

- **Time:** O(n)
- **Space:** O(1)
- **Ignores the sorted property** of the input — wasted information.
- **Will be rejected in the interview.** The spec requires O(log n).
- Kept as the verbal baseline only: *"Brute force is linear scan, O(n) — but I need O(log n), so I'll use binary search."*

---

## 2. Binary Search — RECOMMENDED (O(log n))

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1
```

### How it works (the key invariants)

1. **The target (if it exists) is always within `[left, right]` inclusive.** This is the loop invariant. We never throw away a range that could still contain the target.

2. **Each iteration halves the search range.** That's where O(log n) comes from — `log₂(10⁴) ≈ 14` iterations for the maximum input size.

3. **`<=` in the loop condition (not `<`).** When `left == right`, the range contains exactly ONE element that hasn't been checked yet. Using `<` would skip it — off-by-one trap.

4. **`mid + 1` and `mid - 1` for bounds update.** `mid` has already been checked (it wasn't the target), so it's excluded from the next iteration. Without `+1`/`-1` you'd loop forever on a 2-element range.

### Complexity

- **Time:** O(log n) — halving each step
- **Space:** O(1) — two indices

---

## 3. Comparison

| Aspect              | Linear Scan (O(n)) | Binary Search (O(log n)) | Winner |
|---------------------|---------------------|---------------------------|--------|
| Time                | O(n)                | **O(log n)**              | Binary |
| Space               | O(1)                | O(1)                      | Tie    |
| Uses sorted?        | No                  | **Yes**                   | Binary |
| Ops at n = 10⁴      | ~10,000             | **~14**                   | Binary |
| Ops at n = 1,000,000| ~1,000,000          | **~20**                   | Binary |
| Accepted by spec?   | No                  | **Yes**                   | Binary |

---

## 4. How to Practice This Script (Daily Flow)

### Step 1: Read this explanation out loud (2–3 min)

> "The problem requires O(log n), so linear scan is out — even though it works, it ignores the sorted property.
>
> I'll use binary search. Two indices: `left = 0`, `right = n - 1`. Each iteration I compute `mid = (left + right) // 2`. If `nums[mid] == target`, return mid. If `nums[mid] < target`, the answer is in the right half — `left = mid + 1`. Otherwise it's in the left half — `right = mid - 1`.
>
> Loop condition is `while left <= right` — we keep going while there's still a valid range. The `<=` includes the case where left and right point at the same element; without it we'd skip that final check.
>
> Halving the range each step gives O(log n). For n = 10,000 that's ~14 iterations. O(1) space, just two indices."

### Step 2: Key Points to Memorize

- **`while left <= right`** (not `<`) — final single-element check must run
- **`mid + 1` and `mid - 1`** — mid already checked, exclude it
- **Returns -1** when target doesn't exist
- **`left + (right - left) // 2`** is the overflow-safe expression in languages with bounded ints (Java/C++). Python ints are unbounded, so `(left + right) // 2` is fine — but mention it if asked.
- **The pattern name is "Binary Search"** — not "two pointer," even though it uses two indices

### Step 3: Test Cases

| nums                      | target | Expected | Notes                           |
|---------------------------|--------|----------|---------------------------------|
| `[-1, 0, 3, 5, 9, 12]`    | 9      | 4        | Canonical                       |
| `[-1, 0, 3, 5, 9, 12]`    | 2      | -1       | Not found                       |
| `[5]`                     | 5      | 0        | Single element, hit             |
| `[5]`                     | 1      | -1       | Single element, miss            |
| `[1, 2, 3, 4, 5]`         | 1      | 0        | First element                   |
| `[1, 2, 3, 4, 5]`         | 5      | 4        | Last element                    |
| `[1, 3]`                  | 2      | -1       | Tiny array, miss between values |

### Step 4: Full Testing Code

```python
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1


# ============= TEST CASES =============
solution = Solution()
print(solution.search([-1, 0, 3, 5, 9, 12], 9))   # 4
print(solution.search([-1, 0, 3, 5, 9, 12], 2))   # -1
print(solution.search([5], 5))                    # 0
print(solution.search([5], 1))                    # -1
print(solution.search([1, 2, 3, 4, 5], 1))        # 0
print(solution.search([1, 2, 3, 4, 5], 5))        # 4
```

---

## 5. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| `while left < right` instead of `<=` | Misses the final single-element check | Use `<=` for "find exact match" |
| `left = mid` (no +1) | Infinite loop when range narrows to 2 elements | Always `mid + 1` / `mid - 1` |
| Missing `target` in function signature | Function silently grabs `target` from global scope (LEGB rule). Breaks when imported. | Declare `target: int` as a parameter |
| Calling it "two pointer" | Confuses the interviewer — pattern name is different | Say "Binary Search" |
| Returning `mid` value instead of index | Spec wants the INDEX, not the value | Return `mid`, the index itself |
| Using `/` instead of `//` | Float division gives a non-integer index → TypeError | Use `//` for integer division |

---

## 6. Interview-Ready Out-Loud Explanation

> "Brute force is linear scan, O(n) — but the spec requires O(log n), so I'll use binary search.
>
> Two indices, `left = 0` and `right = n - 1`. Each iteration I check `mid = (left + right) // 2`. Three cases: if `nums[mid] == target`, return mid. If less than target, target is in the right half, so `left = mid + 1`. If greater, target is in the left half, so `right = mid - 1`.
>
> Loop condition is `while left <= right` with `<=` — when `left == right` there's still one element to check; using `<` would skip it. After the loop, target wasn't found, so return -1.
>
> Halving the range each step gives **O(log n) time, O(1) space** — just two indices."

---

**Chain position:** Binary Search is the foundation. Variants reuse this skeleton:
- **Search Insert Position** — returns insertion index when not found
- **Find First and Last Position** — modified to find boundaries
- **Search in Rotated Sorted Array** — adds pivot detection

Master this one cold — the variants are 80% the same code.
