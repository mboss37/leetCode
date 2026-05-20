# LC 238 — Product of Array Except Self · Practice Script

---

## Problem

> Given an integer array `nums`, return an array `answer` where `answer[i]` is the product of **all the elements except `nums[i]`**.
>
> Constraints:
> - Must run in **O(n)**.
> - **No division allowed.**
> - Guaranteed the product fits in a 32-bit integer.

---

## NOT RECOMMENDED — Brute Force (O(n²))

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = []
        for i in range(n):
            product = 1
            for j in range(n):
                if j != i:
                    product *= nums[j]
            result.append(product)
        return result
```

- **Time:** O(n²) — nested loop.
- For n = 10⁵: 10¹⁰ ops → TLE.

**Why not division?** `total / nums[i]` would be O(n), but the spec bans division. It also fails on zeros (and breaks twice on multiple zeros).

State verbally:
> *"Brute force is for each index, loop and multiply all others — O(n²). Division would be O(n) but it's banned and breaks on zeros. I'll split into a left-product pass and a right-product pass — O(n) time, O(1) extra space."*

---

## The key insight

For any index `i`:

```
answer[i] = (product of nums[0..i-1]) × (product of nums[i+1..n-1])
              ^^^^^^^^^^^^^^^^^^^^         ^^^^^^^^^^^^^^^^^^^^^^^^
              "left of i"                  "right of i"
```

If we compute "left product" and "right product" for every `i`, we're done.

---

## RECOMMENDED — Two Passes, O(1) extra space (O(n))

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n

        # Pass 1: result[i] = product of everything LEFT of i.
        left = 1
        for i in range(n):
            result[i] = left
            left *= nums[i]

        # Pass 2: multiply in product of everything RIGHT of i.
        right = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right
            right *= nums[i]

        return result
```

### How it works

**Pass 1** fills `result[i]` with the **left product** — the product of everything BEFORE `i`. For `i = 0`, that's `1` (no elements to the left).

**Pass 2** walks back-to-front maintaining a running **right product**. It multiplies the existing `result[i]` (which is the left product) by the right product. After multiplying, update `right *= nums[i]` for the next iteration.

### Trace on `nums = [1, 2, 3, 4]`

**Pass 1 (left products):**

| i | left before | result[i] | left after |
|---|---|---|---|
| 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 2 |
| 2 | 2 | 2 | 6 |
| 3 | 6 | 6 | 24 |

After Pass 1: `result = [1, 1, 2, 6]`

**Pass 2 (right products), iterating from i=3 down to 0:**

| i | right before | result[i] before | result[i] after | right after |
|---|---|---|---|---|
| 3 | 1 | 6 | 6×1 = 6 | 4 |
| 2 | 4 | 2 | 2×4 = 8 | 12 |
| 1 | 12 | 1 | 1×12 = 12 | 24 |
| 0 | 24 | 1 | 1×24 = 24 | 24 |

Final: `result = [24, 12, 8, 6]` ✓

### Why O(1) extra space

Problem convention: the **output array doesn't count** toward extra space (you have to return SOMETHING). We use only two scalar accumulators (`left`, `right`) on top of that.

A naïve version uses two extra arrays for left/right products — O(n) extra. Our trick: write the left products directly into `result`, then weave in the right products on the way back.

### Complexity

- **Time:** O(n) — two passes
- **Space:** O(1) — not counting the required output

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Initializing `left = 0` | Everything becomes 0 | `left = 1` (multiplicative identity) |
| Using division | Banned by spec; breaks on zeros | Two-pass left/right |
| Writing nested loops | O(n²) → TLE | Two SEPARATE passes |
| Forgetting to update `right *= nums[i]` AFTER using it | Off-by-one — current index's value contaminates | Update AFTER multiplying into result |
| Using two extra arrays | Costs O(n) extra space | Reuse `result` |

---

## Zero handling — works for free

| nums | result |
|---|---|
| `[0, 0]` | `[0, 0]` |
| `[-1, 1, 0, -3, 3]` | `[0, 0, 9, 0, 0]` |

Why? If there's exactly one zero at position `z`:
- Every `result[i]` for `i != z` includes the zero in either its left or right product → 0.
- `result[z]` is left × right where neither includes the zero → product of all non-zeros.

If there are 2+ zeros, every entry is 0. No special-casing needed.

---

## Interview Out-Loud

> "Brute force is O(n²) — for each index multiply all others. Division would be O(n) but it's banned and breaks on zeros.
>
> Insight: answer[i] = (product of everything LEFT of i) × (product of everything RIGHT of i).
>
> Two passes:
> Pass 1: walk left-to-right. result[i] = running left product (product of everything before i). For i=0 that's 1.
> Pass 2: walk right-to-left. Multiply result[i] by a running right product.
>
> O(n) time, O(1) extra space — the output array isn't counted.
>
> Zeros handled automatically: one zero gives all-zeros except at the zero's index. Two zeros give all-zeros."

---

**Chain position:** Prefix-suffix product pattern. Same skeleton as: Prefix Sum, Trapping Rain Water (with maxes instead of products).
