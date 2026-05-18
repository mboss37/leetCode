# Practice script: docs/exercise_scripts/LC322_CoinChange_practice.md

from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # Bottom-up DP.
        #   dp[a] = fewest coins needed to make amount a, or INF if impossible.
        #
        # For every amount from 1..amount, try every coin denomination.
        # If we can use coin c (c <= a), the answer for a is at most
        # dp[a - c] + 1 (we use one coin c on top of dp[a-c]).
        # Take the min over all coins.

        INF = float("inf")
        dp = [INF] * (amount + 1)
        dp[0] = 0   # 0 coins needed to make amount 0

        for a in range(1, amount + 1):
            for c in coins:
                if c <= a:
                    dp[a] = min(dp[a], dp[a - c] + 1)

        return dp[amount] if dp[amount] != INF else -1


# ============= TEST CASES =============
solution = Solution()

print(solution.coinChange([1, 2, 5], 11))        # 3  (5+5+1)
print(solution.coinChange([2], 3))               # -1 (impossible)
print(solution.coinChange([1], 0))               # 0
print(solution.coinChange([1], 2))               # 2
print(solution.coinChange([1, 2, 5], 100))       # 20 (twenty 5s)
print(solution.coinChange([186, 419, 83, 408], 6249))  # 20
