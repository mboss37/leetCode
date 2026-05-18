# Practice script: docs/exercise_scripts/LC34_FindFirstAndLastPosition_practice.md

from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        LINEAR SCAN — NOT RECOMMENDED.

        Time:  O(n)
        Space: O(1)

        Spec requires O(log n). This is rejected in an interview because
        it ignores the sorted property. Kept here as the verbal baseline
        ("brute force is linear, O(n); I'll use two binary searches for O(log n)").
        """
        first = -1
        last = -1
        for i, num in enumerate(nums):
            if num == target:
                if first == -1:        # only set first the very first time
                    first = i
                last = i               # always update last on every match
        return [first, last]


# ============= TEST CASES =============
sol = Solution()

print(sol.searchRange([5, 7, 7, 8, 8, 10], 8))     # [3, 4]
print(sol.searchRange([5, 7, 7, 8, 8, 10], 6))     # [-1, -1]
print(sol.searchRange([], 0))                       # [-1, -1]
print(sol.searchRange([2, 2], 2))                   # [0, 1]
