# LC 11 — Container With Most Water · Practice Script

**Chain:** Two Sum Sorted (converging two pointers) → **Container With Most Water** (greedy two pointers)

---

## Problem

> Given `n` non-negative integers `height[i]` representing vertical lines at x-coordinates 0..n−1, find two lines that together with the x-axis form a container holding the most water. Return the **maximum amount of water**.

**Constraints:**
- `n == height.length`
- `2 <= n <= 10⁵`
- `0 <= height[i] <= 10⁴`

**Area formula:**

```
area = width × height
     = (right - left) × min(height[left], height[right])
```

Width = index distance. Height = the **shorter** of the two lines (water spills over the shorter side).

---

## 1. NOT RECOMMENDED — Brute Force (O(n²))

```python
class Solution:
    def maxArea(self, heights: List[int]) -> int:
        max_area = 0
        for i in range(len(heights)):
            for j in range(i + 1, len(heights)):
                area = (j - i) * min(heights[i], heights[j])
                if area > max_area:
                    max_area = area
        return max_area
```

- **Time: O(n²)** — try every pair
- **Space: O(1)**
- **Rejected by judge.** n = 10⁵ → 10¹⁰ ops → guaranteed TLE.

State it verbally:
> *"Naive is every pair, O(n²). For n = 10⁵ that's 10 billion ops — TLE. I'll use the two-pointer greedy for O(n)."*

---

## 2. RECOMMENDED — Two-pointer Greedy (O(n))

```python
from typing import List

class Solution:
    def maxArea(self, heights: List[int]) -> int:
        max_area = 0
        left, right = 0, len(heights) - 1

        while left < right:
            area = (right - left) * min(heights[left], heights[right])
            max_area = max(max_area, area)

            # Move the shorter side inward.
            if heights[left] < heights[right]:
                left += 1
            else:
                right -= 1

        return max_area
```

### The greedy proof — "always move the shorter side"

Why does moving only the **shorter** side find the optimal answer?

Imagine the current pair is `(L, R)` with `heights[L] < heights[R]`. Consider what happens if we moved R (the taller) instead:
- Width strictly decreases (R moves left, L stays).
- Height is `min(heights[L], heights[new R])`. Since `heights[L]` is the shorter one and L is unchanged, the height is **at most `heights[L]`** (the cap).
- Result: width down, height ≤ same → area ≤ same.

So moving the taller side can **never improve** the answer. Moving the shorter side is the ONLY way to potentially gain height that outweighs the width loss.

When heights are **equal**, moving either is fine (the tie case is provably tolerant — see practice notes).

### Why O(n)

Each iteration advances exactly one pointer (or both in a tie). The pointers start at opposite ends and converge. **Total iterations ≤ n.**

### Trace on `[1, 8, 6, 2, 5, 4, 8, 3, 7]`

| L | R | h[L] | h[R] | width | area | max | move |
|---|---|---|---|---|---|---|---|
| 0 | 8 | 1 | 7 | 8 | 8 | 8 | L (1 < 7) |
| 1 | 8 | 8 | 7 | 7 | **49** | **49** | R (8 > 7) |
| 1 | 7 | 8 | 3 | 6 | 18 | 49 | R |
| 1 | 6 | 8 | 8 | 5 | 40 | 49 | R (tie → right) |
| 1 | 5 | 8 | 4 | 4 | 16 | 49 | R |
| 1 | 4 | 8 | 5 | 3 | 15 | 49 | R |
| 1 | 3 | 8 | 2 | 2 | 4 | 49 | R |
| 1 | 2 | 8 | 6 | 1 | 6 | 49 | R |
| 1 | 1 → exit |

Returns **49** ✓

### Complexity

- **Time: O(n)** — pointers converge, each moves ≤ n times total.
- **Space: O(1)** — just two indices and a max.

---

## 3. Comparison

| Approach | Time | Space | n=10⁵ | Accepted? |
|---|---|---|---|---|
| Brute force pairs | O(n²) | O(1) | ~10¹⁰ ops | ❌ TLE |
| **Two-pointer greedy** | **O(n)** | **O(1)** | ~10⁵ ops | **✓** |

---

## 4. How to Practice

### Step 1: Read out loud

> "Naive is every pair, O(n²) — for n = 10⁵ that's TLE territory. Better: two-pointer greedy from both ends, O(n).
>
> Compute the current area: width is the index difference, height is the SHORTER of the two lines. Update max. Then move the shorter pointer inward — because moving the taller never helps (width shrinks, height capped by shorter line, area can only decrease).
>
> Each pointer moves at most n times, so total is O(n). O(1) space — just two indices."

### Step 2: Key Points

- **Width** is the INDEX difference (`right - left`), not the height difference.
- **Height** is `min(heights[left], heights[right])` — water spills over the shorter.
- **Always move the SHORTER side.** Moving the taller can never improve the answer.
- **`while left < right`** — strict inequality, the pointers can't be at the same position.
- **Tie case** (equal heights): move either — the algorithm is tie-tolerant.

### Step 3: Test Cases

| heights | Expected | Notes |
|---|---|---|
| `[1, 8, 6, 2, 5, 4, 8, 3, 7]` | 49 | Canonical (indices 1 & 8) |
| `[1, 1]` | 1 | Minimum size |
| `[4, 3, 2, 1, 4]` | 16 | Tallest pair at the ends (indices 0 & 4) |
| `[1, 2, 1]` | 2 | Single peak in middle |
| `[1, 7, 2, 5, 4, 7, 3, 6]` | 36 | Multiple candidates |
| `[5, 4, 3, 1, 1, 1]` | 6 | Decreasing — shorter side keeps moving |
| `[5, 5, 100, 5]` | 15 | Equal-end case + taller inside |

---

## 5. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Moving BOTH pointers on `heights[left] != heights[right]` | Skips pairs where the taller side still has value | Move ONLY the shorter side |
| `elif heights[right] > heights[left]` as second branch | Same condition as the `if` (mathematically identical) — never fires; falls to else | `elif heights[left] > heights[right]` — flip an operand |
| Using `height` difference for width | Width is INDEX difference, not value difference | `right - left`, not `heights[right] - heights[left]` |
| Forgetting `min()` for the height | Used `max()` or one of the heights — water spills over shorter | `min(heights[left], heights[right])` |
| `while left <= right` | Pointers can be equal → width 0 → wasted iteration | Use `while left < right` strictly |

---

## 6. Interview Out-Loud Explanation

> "Brute force is every pair, O(n²). For n up to 10⁵ that's 10 billion ops — TLE.
>
> Better: two-pointer greedy. Start at both ends. Compute area = width × min of heights. Update max. Then move the SHORTER side inward.
>
> Why always the shorter? Because moving the taller cannot help: width shrinks, and the height is already capped by the shorter line — it can't go above that no matter what we pair the taller with. Only moving the shorter has any chance of finding a taller-than-current-shorter partner.
>
> Each pointer moves at most n times total, so O(n) time, O(1) space."

---

**Chain position:** Container With Most Water is the **"greedy two-pointer"** pattern. Same shape extends to:
- **Trapping Rain Water** — two pointers, track max heights on each side
- **Squares of a Sorted Array** — two pointers, fill output from the back
- **3Sum / 3Sum Closest** — outer loop + two-pointer scan inside

The reflex: when you see "two endpoints + optimize a function of both" → reach for two pointers, decide direction by the comparison.
