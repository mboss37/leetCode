# LC 35 — Search Insert Position · Practice Script

**Code:** [code/searchInsert/](../../code/searchInsert/)

**Chain:** Binary Search → **Search Insert Position** → Find First and Last Position

---

## Problem

> Given a **sorted** array of **distinct** integers `nums` and a target value, return the **index** where `target` is found. If not found, return the index where it **would be** inserted to keep the array sorted.
>
> You must write an algorithm with **O(log n) runtime complexity**.

**Constraints:**
- `1 <= nums.length <= 10⁴`
- `-10⁴ <= nums[i] <= 10⁴`
- `nums` contains **distinct** values, sorted ascending.
- `-10⁴ <= target <= 10⁴`

**Key difference from Binary Search:** when target is NOT in the array, instead of returning `-1` we return **the insertion index**.

---

## 1. Linear Scan — NOT RECOMMENDED (O(n))

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        for i, value in enumerate(nums):
            if value >= target:
                return i
        return len(nums)
```

- **Time:** O(n)
- **Space:** O(1)
- **`>=` handles both cases in one check:**
  - `value == target` → exact match index
  - `value > target` → insertion index (target goes here)
- **`return len(nums)`** if nothing is `>= target` → insert at the end.
- **Rejected in the interview** because spec requires O(log n).

---

## 2. Binary Search — RECOMMENDED (O(log n))

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
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

        return left   # ← THE ONLY CHANGE FROM PLAIN BINARY SEARCH
```

### The one-line change from plain Binary Search

| | Plain Binary Search | Search Insert Position |
|---|---|---|
| Final return | `return -1` | `return left` |

Everything else is identical. The loop, the three-branch logic, the `<=` boundary — all the same.

### Why `left` is the correct insertion index when the loop exits

When `while left <= right` exits, it's because `left > right`. Two invariants held throughout the loop:

1. **`left` has been moved past every index where `nums[idx] < target`.**
2. **`right` has been moved before every index where `nums[idx] > target`.**

When the loop ends, `left` is sitting exactly at the first index where the value is `>= target` — that's the insertion position. (If target was greater than every element, `left` ends up at `len(nums)`.)

### Common trap (the bug from today's first attempt)

```python
if nums[mid] >= target:
    return mid        # ← WRONG — returns the first mid that hits >= target,
                      #   not the leftmost such position
```

This fails when target exists at an index smaller than the mid binary search lands on. Example: `nums = [-1, 0, 3, 5, 9, 12]`, target = 5 — first mid is 2 (value 3), then mid=4 (value 9), returns 4 instead of 3.

**Fix:** separate the cases. `==` returns mid. `>` keeps narrowing (`right = mid - 1`).

### Complexity

- **Time:** O(log n) — halving each step
- **Space:** O(1)

---

## 3. Comparison

| Aspect              | Linear (O(n))         | Binary Search (O(log n)) | Winner |
|---------------------|------------------------|---------------------------|--------|
| Time                | O(n)                   | **O(log n)**              | Binary |
| Space               | O(1)                   | O(1)                      | Tie    |
| Uses sorted?        | No                     | **Yes**                   | Binary |
| Accepted by spec?   | No                     | **Yes**                   | Binary |

---

## 4. How to Practice This Script

### Step 1: Read this aloud (1 min)

> "It's Binary Search with one change — when the loop exits without finding the target, I return `left` instead of `-1`. That `left` index is exactly where target would be inserted to keep the array sorted.
>
> The skeleton is identical to Binary Search: `left = 0`, `right = n-1`, `while left <= right`, three branches on the mid comparison. The only difference is the final return statement."

### Step 2: Key Points

- **Skeleton is identical to Binary Search.** Memorize once, use twice.
- **Final return: `left`** (not `-1`).
- **Don't conflate `==` and `>`.** They're different cases — `==` returns mid, `>` narrows from the right.

### Step 3: Test Cases

| nums          | target | Expected | Notes                          |
|---------------|--------|----------|--------------------------------|
| `[1, 3, 5, 6]`| 5      | 2        | Exact match                    |
| `[1, 3, 5, 6]`| 2      | 1        | Insert between 1 and 3         |
| `[1, 3, 5, 6]`| 7      | 4        | Insert at end                  |
| `[1, 3, 5, 6]`| 0      | 0        | Insert at start                |
| `[1]`         | 0      | 0        | Single element, before         |
| `[1]`         | 2      | 1        | Single element, after          |
| `[1, 3]`      | 3      | 1        | Match at end                   |

---

## 5. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| `if nums[mid] >= target: return mid` | Returns the first mid hit, not the leftmost valid position. Fails when target IS in the array and binary search lands on a higher mid first. | Split into `==` (return) and `>` (narrow right). |
| Returning `-1` at the end | That's plain Binary Search. Wrong for this problem. | `return left` |
| `while left < right` instead of `<=` | Misses single-element check | `<=` |
| Missing `target` in function signature | Function silently grabs from global scope | Declare it as a parameter |

---

## 6. Interview Out-Loud Explanation

> "This is Binary Search with one change — same skeleton, but when the loop exits without finding the target, I return `left` instead of `-1`.
>
> The reasoning: when the `while left <= right` loop exits, `left` has been advanced past every index holding a value smaller than target, and `right` has been pulled before every index holding a value greater. So `left` sits exactly at the position where target should be inserted to keep things sorted.
>
> Time O(log n), space O(1)."

---

**Chain position:** Skeleton reuse from Binary Search. The next problem in the chain — Find First and Last Position — extends this further (two binary searches: one for the leftmost occurrence, one for the rightmost).
