# LC 121 — Best Time to Buy and Sell Stock · Practice Script

**Problem:**  
You are given an array `prices` where `prices[i]` is the price of a given stock on day `i`.  
You want to maximize profit by buying on one day and selling on a later day. Return the maximum profit. If no profit possible, return 0.

---

## Solution 1: Brute Force (Two Nested Loops)

```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        
        for i in range(len(prices)):                    # buy day
            for j in range(i + 1, len(prices)):         # sell day (must be after buy)
                profit = prices[j] - prices[i]
                if profit > max_profit:
                    max_profit = profit
        
        return max_profit
```

**Time Complexity:** O(n²)  
**Space Complexity:** O(1)

### Why this is NOT recommended

- Extremely slow for large inputs (e.g. 10,000 days = ~50 million operations)
- Interviewers expect the optimal O(n) solution for this classic problem
- Does not demonstrate efficient algorithm thinking

---

## Solution 2: Optimal One-Pass (Compact) — Recommended

```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0

        max_profit = 0
        min_buy = prices[0]

        for sell in prices:
            max_profit = max(max_profit, sell - min_buy)
            min_buy = min(min_buy, sell)

        return max_profit
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

### Trace on `prices = [7, 1, 5, 3, 6, 4]`

| sell | min_buy (before) | profit = sell − min_buy | max_profit (after) | min_buy (after) |
|------|------------------|--------------------------|---------------------|------------------|
|  7   | 7                |  0                       | 0                   | 7                |
|  1   | 7                | -6 (max keeps 0)         | 0                   | **1** (new low)  |
|  5   | 1                |  4                       | **4**               | 1                |
|  3   | 1                |  2                       | 4                   | 1                |
|  6   | 1                |  **5**                   | **5**               | 1                |
|  4   | 1                |  3                       | 5                   | 1                |

Result: `5`. Watch row 2 — when today is the new minimum, profit is negative but `max(...)` ignores it; we just update `min_buy` for tomorrow. **Compute profit first, then update min** — otherwise day-zero would subtract itself.

---

### Why Solution 2 is RECOMMENDED

- Only **one single pass** through the array
- Very compact and elegant
- Classic "track minimum so far" pattern (very common in interviews)
- Optimal time and space
- Clean and professional
- Shows you can optimize from O(n²) to O(n)

---

### Comparison

| Aspect                  | Brute Force (Solution 1)     | One-Pass Compact (Solution 2) | Winner          |
|-------------------------|------------------------------|-------------------------------|-----------------|
| Time Complexity         | O(n²)                        | **O(n)**                      | Solution 2      |
| Space Complexity        | O(1)                         | O(1)                          | Tie             |
| Interview Signal        | Weak                         | **Strong**                    | Solution 2      |
| Ease of Explanation     | Medium                       | **Easy**                      | Solution 2      |

---

## Interview Out-Loud

> "The brute force approach checks every possible buy and sell pair, which is O(n²).  
> Instead, I do one single pass while keeping track of the minimum buy price seen so far.  
> At each day (as potential sell day), I calculate the profit using the current min_buy, then update min_buy if today's price is cheaper.  
> This solves the problem in O(n) time and O(1) space."

---

## Test Cases

| Input                  | Expected Output | Explanation                          |
|------------------------|-----------------|--------------------------------------|
| `[7,1,5,3,6,4]`        | 5               | Buy at 1, sell at 6                  |
| `[7,6,4,3,1]`          | 0               | Prices only decrease → no profit     |
| `[1]`                  | 0               | Only one day                         |
| `[]`                   | 0               | Empty input                          |
| `[3,1,12,50]`          | 49              | Buy at 1, sell at 50                 |
| `[2,4,1]`              | 2               | Buy at 2, sell at 4                  |

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Updating `min_buy` BEFORE computing profit | Profit becomes 0 (today's price minus today's price) | Compute `max_profit` FIRST, then update `min_buy` |
| Initializing `min_buy = 0` | Profit gets inflated (price minus 0) for the first day | Initialize `min_buy = prices[0]` OR `float('inf')` |
| Returning a negative profit | Spec says return 0 if no profit possible | Initialize `max_profit = 0` — won't go below |
| `for i, sell in enumerate(prices):` and using `i` unnecessarily | Code smell — `enumerate` when you don't need the index | `for sell in prices:` — cleaner |
| Two-pass solution (find min, then find max after) | O(n) but misses days where min appears after | Single pass — min so far, profit at each day |

---

## Chain position

Best Time to Buy/Sell is the **Greedy** pattern — one linear walk, two scalar trackers (`min_so_far` and `max_profit`), no window and no DP table. The greedy choice (always buy at the cheapest valid day so far, take the best profit seen) provably gives the global optimum. The "best ending at day i" idea extends to:
- **Maximum Subarray** (Kadane's) — same shape, different update rule
- **Best Time to Buy/Sell II** — multiple transactions allowed
- **Container With Most Water** — track best as you walk
- **Maximum Product Subarray** — same one-pass shape with two trackers (min + max)

This is the **simplest dynamic-programming pattern** — "best ending here, best overall" — without explicitly building a DP array. Lock it in.
