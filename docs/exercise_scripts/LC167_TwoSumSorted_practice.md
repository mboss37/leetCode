# LC 167 — Two Sum II · Input Array Is Sorted · Practice Script

**Code:** [code/twoSumSorted/](../../code/twoSumSorted/)

**Chain:** Two Sum → **Two Sum Sorted** → 3Sum → 3Sum Closest

---

## Problem

> Given a **1-indexed** array of integers `numbers` that is already **sorted in non-decreasing order**, find two numbers such that they add up to a specific `target` number. Return the indices of the two numbers as a 1-indexed array `[index1, index2]`.
>
> Tests are generated such that there is **exactly one solution**. You may not use the same element twice.
>
> Your solution must use only **constant extra space**.

**Constraints:**
- `2 <= numbers.length <= 3 * 10⁴`
- `-1000 <= numbers[i] <= 1000`
- `numbers` is sorted ascending.
- `-1000 <= target <= 1000`

**Two critical wrinkles:**
1. **1-indexed return** (NOT 0-indexed) — easy to miss.
2. **Constant space** — rules out hash maps (which Two Sum used).

---

## 1. Brute Force (O(n²)) — verbal baseline only

```python
class Solution:
    def twoSum(self, numbers, target):
        n = len(numbers)
        for i in range(n):
            for j in range(i + 1, n):
                if numbers[i] + numbers[j] == target:
                    return [i + 1, j + 1]   # 1-indexed
        return []
```

- **Time:** O(n²) — two nested loops.
- **Space:** O(1).
- Ignores the **sorted** property completely.
- State verbally, don't write in the interview.

---

## 2. RECOMMENDED — Converging Two Pointers (O(n), O(1) space)

```python
from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]

            if current_sum == target:
                return [left + 1, right + 1]   # 1-indexed!
            elif current_sum < target:
                left += 1     # need a bigger sum → move left right
            else:
                right -= 1    # need a smaller sum → move right left

        return []   # spec guarantees a solution, so this is defensive only
```

### Why this works (the invariant)

> **At the top of every loop iteration, the answer pair (if it exists in the unexplored range) lies somewhere between `left` and `right`, inclusive.**

Every pointer move is provably safe:
- **Sum too small** → the value at `left` is too small to be in the answer. ANY pair involving it would also be too small (since `right` only decreases from here on). So `left` can be discarded → `left += 1`.
- **Sum too big** → mirror argument: `right` is too big to be in any answer → `right -= 1`.

Each step eliminates exactly one position. After at most `n` iterations, we either find the answer or the pointers collide.

### The "sorted" property is everything

This invariant ONLY holds because the array is sorted. Without sorted order, you can't tell which direction to move — that's why Two Sum (unsorted) needs a hash map instead.

### Complexity

- **Time:** O(n) — each pointer moves at most n times in total.
- **Space:** O(1) — just two integer indices.

---

## 3. Comparison: Brute Force vs Two-Pointer

| Aspect | Brute Force (O(n²)) | Two-Pointer (O(n)) | Winner |
|---|---|---|---|
| Time | O(n²) | **O(n)** | Two-Pointer |
| Space | O(1) | O(1) | Tie |
| Uses sorted property | No | **Yes** | Two-Pointer |
| Lines of code | ~7 | ~10 | Brute |
| At n = 30,000 | ~450M ops | ~30K ops | Two-Pointer |

---

## 4. The Trap — 1-indexed Return

Easy to forget:
```python
return [left, right]         # ✗ WRONG — 0-indexed
return [left + 1, right + 1] # ✓ CORRECT — 1-indexed
```

LeetCode's spec is unusual here. Most array problems are 0-indexed; Two Sum Sorted asks for **1-indexed**. Add `+ 1` to both pointer values in the return statement.

---

## 5. How to Practice

### Step 1: Read out loud

> "Input is sorted, and I need O(1) extra space — that rules out a hash map. The sorted property unlocks the two-pointer pattern.
>
> Put left at index 0 and right at the last index. Compute the sum. If it equals target, return [left+1, right+1] — the spec wants 1-indexed.
>
> If the sum is too small, the smallest value is at left, so advance left right. If too big, advance right left. Each move provably eliminates one position. Each pointer moves at most n times → O(n)."

### Step 2: Key Points

- **`while left < right`** (NOT `<=`) — same element can't be used twice, so the pointers must stop before they collide.
- **Return `[left + 1, right + 1]`** — 1-indexed.
- **Three branches**: equal (return), less than target (left++), greater than target (right--).
- **Defensive `return []`** at the end — spec guarantees a solution but it's a good habit. State this verbally.

### Step 3: Test Cases

| numbers              | target | Expected | Notes |
|----------------------|--------|----------|-------|
| `[2, 7, 11, 15]`     | 9      | `[1, 2]` | Canonical |
| `[2, 3, 4]`          | 6      | `[1, 3]` | Pair around middle |
| `[-1, 0]`            | -1     | `[1, 2]` | Tiny array, negatives |
| `[5, 25, 75]`        | 100    | `[2, 3]` | Pair at end |
| `[1, 2, 3, 4, 4, 9]` | 8      | `[4, 5]` | Duplicate value — still 1 unique pair |

---

## 6. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Returning 0-indexed | Off-by-one rejection | `[left + 1, right + 1]` |
| `while left <= right` | Same element used twice | Use `<` strictly |
| Forgetting the sorted property → reaching for hash map | Wastes O(n) space | Use two pointers — that's the whole point |
| `current_sum > target` branch missing | Infinite loop on big sums | Add the third branch with `right -= 1` |

---

## 7. Interview Out-Loud Explanation

> "Brute force is two nested loops, O(n²). But the array is sorted and I need O(1) extra space — that means hash maps are out. The sorted property unlocks the two-pointer pattern.
>
> Two indices: left at 0, right at n-1. While left is less than right (they can't reuse the same element), compute the sum. If it equals target, return both indices 1-indexed. If the sum is too small, left advances right — bigger value. If too big, right advances left — smaller value.
>
> Each step eliminates exactly one candidate position. Time: O(n). Space: O(1). The spec guarantees a solution so I won't reach the fallback, but I'll add a defensive return at the end."

---

**Chain position:** This skeleton is reused in:
- **3Sum**: sort, then outer loop + this two-pointer pattern for each anchor.
- **3Sum Closest**: same skeleton, distance tracker instead of dedup.
- **Container With Most Water**: two pointers, greedy "move shorter side."
- **Valid Palindrome**: two pointers on a string, meet in middle.

Master the converging two-pointer invariant here — it's the foundation for five other Phase A/B problems.
