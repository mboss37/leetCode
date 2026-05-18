# LC 322 — Coin Change · Practice Script

---

## Problem

> Given coin denominations `coins` and an integer `amount`, return the **fewest number of coins** to make `amount`. If impossible, return `-1`. You have unlimited coins of each denomination.

**Constraints:**
- `1 <= coins.length <= 12`
- `1 <= coins[i] <= 2³¹ - 1`
- `0 <= amount <= 10⁴`

---

## Why NOT greedy

> "Take the biggest coin that fits, repeat."

Counterexample: `coins = [1, 3, 4]`, `amount = 6`.
- Greedy: 4 + 1 + 1 = **3 coins**
- Optimal: 3 + 3 = **2 coins**

Greedy can be off arbitrarily. **You need DP.**

---

## NOT RECOMMENDED — Pure Recursion (Exponential)

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        def best(a):
            if a == 0: return 0
            if a < 0:  return float('inf')
            return min(best(a - c) for c in coins) + 1
        ans = best(amount)
        return ans if ans != float('inf') else -1
```

- **Time:** O(c^a) — branching factor `c` (number of coins), depth `a` (amount). Recomputes the same subproblems millions of times.
- For amount = 100, coins = [1,2,5]: easily 10⁹+ recursive calls → TLE.

State verbally:
> *"Naive recursion is exponential — same subproblems get recomputed over and over. I'll add memoization (or go bottom-up with a DP array) to bring it down to O(amount × len(coins))."*

---

## RECOMMENDED — Bottom-Up DP (O(amount × len(coins)))

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        INF = float('inf')
        dp = [INF] * (amount + 1)
        dp[0] = 0
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a:
                    dp[a] = min(dp[a], dp[a - c] + 1)
        return dp[amount] if dp[amount] != INF else -1
```

### The key idea

**`dp[a]` = fewest coins to make amount `a`.**

**Recurrence:**
```
dp[a] = 1 + min(dp[a - c] for c in coins if c <= a)
```

In English: "to make amount `a`, the LAST coin you used was some `c`. Before placing it, you had made `a - c`. So the best you can do is 1 + the best way to make `a - c`. Try every coin and take the min."

**Base case:** `dp[0] = 0` (zero coins to make zero).

### Trace on `coins = [1, 2, 5]`, `amount = 6`

| a | tries (dp[a-c] + 1) | dp[a] |
|---|---|---|
| 0 | — | 0 |
| 1 | dp[0]+1 = 1 | 1 |
| 2 | dp[1]+1=2, dp[0]+1=1 | 1 |
| 3 | dp[2]+1=2, dp[1]+1=2 | 2 |
| 4 | dp[3]+1=3, dp[2]+1=2 | 2 |
| 5 | dp[4]+1=3, dp[3]+1=3, dp[0]+1=1 | 1 |
| 6 | dp[5]+1=2, dp[4]+1=3, dp[1]+1=2 | **2** ✓ (5+1) |

### Why this is correct

The recurrence is **optimal-substructure**: the best way to make `a` includes the best way to make `a - c` for some last coin `c`. We try every possible last coin and pick the min.

Order matters: we compute `dp[a]` only AFTER all smaller `dp[*]` are final. That's why we go bottom-up from 1 to `amount`.

### Complexity

- **Time:** O(amount × len(coins))
- **Space:** O(amount)

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Using greedy ("biggest coin first") | Wrong on `[1,3,4]` → 6 | DP — try all combinations |
| Initializing dp[0] = INF | All amounts become INF — answer -1 always | dp[0] = 0 |
| Returning dp[amount] without the INF check | Returns garbage when impossible | Check `dp[amount] != INF` |
| Outer loop over coins, inner over amounts | Subtly different (this gives "number of ways", not "min coins") for some variants — but for THIS problem, either order works | Stay consistent; amount-outer is canonical |
| `dp = [INF] * amount` (missing the +1) | IndexError at `dp[amount]` | `amount + 1` length |

---

## ALTERNATIVE — Top-Down Memoized Recursion (same complexity)

```python
from functools import lru_cache

class Solution:
    def coinChange(self, coins, amount):
        @lru_cache(maxsize=None)
        def best(a):
            if a == 0: return 0
            if a < 0:  return float('inf')
            return min(best(a - c) for c in coins) + 1
        ans = best(amount)
        return ans if ans != float('inf') else -1
```

Some people find this more natural. Same O.

---

## Interview Out-Loud

> "Greedy doesn't work — counterexample coins [1,3,4] amount 6.
>
> Bottom-up DP. dp[a] is the fewest coins to make a. Base case dp[0]=0. For each a from 1 to amount, try every coin c that fits (c ≤ a). The answer for a is the minimum over all coins of dp[a-c] + 1 — meaning we used coin c on top of the best solution for a-c.
>
> If dp[amount] stayed INF, return -1; otherwise return it.
>
> O(amount × number of coins) time, O(amount) space."

---

**Chain position:** Bottom-up DP "fewest steps" pattern. Same shape in: Perfect Squares, Min Cost Climbing Stairs, Word Break (boolean variant).
