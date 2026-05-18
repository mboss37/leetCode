# Practice script: docs/exercise_scripts/LC11_ContainerWithMostWater_practice.md

from typing import List


class Solution:
    def maxArea(self, heights: List[int]) -> int:
        # Greedy two-pointer. Start at both ends, always move the SHORTER side.
        # Why: moving the taller side can never help (width shrinks, and height
        # is already capped by the shorter line — can't exceed that).
        # Only moving the shorter gives any chance of finding a taller pair.

        max_area = 0
        left, right = 0, len(heights) - 1

        while left < right:
            # Area = width × min(left_height, right_height)
            # Water spills over the shorter line, so height = the shorter one.
            area = (right - left) * min(heights[left], heights[right])
            max_area = max(max_area, area)

            # Move the shorter side inward. If tied, move either (we pick right).
            if heights[left] < heights[right]:
                left += 1
            else:
                right -= 1

        return max_area


# ============= TEST CASES =============
solution = Solution()

print(solution.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))   # 49 (indices 1 & 8)
print(solution.maxArea([1, 1]))                         # 1
print(solution.maxArea([4, 3, 2, 1, 4]))                # 16 (indices 0 & 4)
print(solution.maxArea([1, 2, 1]))                      # 2  (indices 0 & 2)
print(solution.maxArea([1, 7, 2, 5, 4, 7, 3, 6]))       # 36 (indices 1 & 7)
print(solution.maxArea([5, 4, 3, 1, 1, 1]))             # 6  (indices 0 & 2)
print(solution.maxArea([5, 5, 100, 5]))                 # 15 (indices 0 & 3)
