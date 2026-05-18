# Practice script: docs/exercise_scripts/LC11_ContainerWithMostWater_practice.md
#
# NOT the version to lead with — O(n²) for n up to 10⁵ = 10¹⁰ ops = TLE.
# Lead with the two-pointer greedy version (container-with-most-water-recommended.py).
# Kept here as the verbal baseline only.

from typing import List


class Solution:
    def maxArea(self, heights: List[int]) -> int:
        """
        BRUTE FORCE — try every pair.

        Time:  O(n²)
        Space: O(1)

        For n up to 10⁵ (LC 11's max), that's 10¹⁰ operations — way too slow,
        guaranteed TLE on any judge. State this verbally as the naive baseline,
        then switch to the two-pointer greedy for O(n).
        """
        max_area = 0
        n = len(heights)

        for i in range(n):
            for j in range(i + 1, n):
                area = (j - i) * min(heights[i], heights[j])
                if area > max_area:
                    max_area = area

        return max_area


# ============= TEST CASES =============
solution = Solution()

print(solution.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))   # 49
print(solution.maxArea([1, 1]))                         # 1
print(solution.maxArea([4, 3, 2, 1, 4]))                # 16
