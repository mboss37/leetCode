# Practice script: docs/exercise_scripts/LC739_DailyTemperatures_practice.md

from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        # Monotonic stack: store INDICES of days whose answer we haven't found yet.
        # Stack stays in decreasing order of temperatures (from bottom to top).
        # When a warmer day arrives, it resolves every day on top of the stack
        # that's colder than it.

        n = len(temperatures)
        result = [0] * n   # default 0 = no warmer day in the future
        stack = []         # holds indices

        for i, t in enumerate(temperatures):
            # While the current day is warmer than the day at the top of the stack,
            # pop that index and record the distance to the current day.
            while stack and temperatures[stack[-1]] < t:
                prev_idx = stack.pop()
                result[prev_idx] = i - prev_idx
            stack.append(i)

        # Any indices left on the stack get result 0 (already initialized).
        return result


# ============= TEST CASES =============
solution = Solution()

print(solution.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))
# Expected: [1, 1, 4, 2, 1, 1, 0, 0]

print(solution.dailyTemperatures([30, 40, 50, 60]))
# Expected: [1, 1, 1, 0]

print(solution.dailyTemperatures([30, 60, 90]))
# Expected: [1, 1, 0]
