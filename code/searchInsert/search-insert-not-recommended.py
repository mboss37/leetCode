# Practice script: docs/exercise_scripts/LC35_SearchInsertPosition_practice.md

from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        LINEAR SCAN — NOT RECOMMENDED.

        Time:  O(n)
        Space: O(1)

        The problem requires O(log n). Linear scan would be REJECTED in
        the interview because it ignores the sorted property of the input.
        Kept here as the verbal baseline only.
        """
        # Walk the array. First position where value is >= target is the answer.
        # Covers both cases:
        #   - value == target: exact match (return that index)
        #   - value > target:  insertion point (target goes just before this index)
        # If we never find such a position, target is bigger than all → insert at end.
        for i, value in enumerate(nums):
            if value >= target:
                return i
        return len(nums)


# ============= TEST CASES =============
solution = Solution()

print(solution.searchInsert([1, 3, 5, 6], 5))   # 2
print(solution.searchInsert([1, 3, 5, 6], 2))   # 1
print(solution.searchInsert([1, 3, 5, 6], 7))   # 4
print(solution.searchInsert([1, 3, 5, 6], 0))   # 0
