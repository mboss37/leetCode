# Practice script: docs/exercise_scripts/LC704_BinarySearch_practice.md

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        LINEAR SCAN — NOT RECOMMENDED.

        Time:  O(n)
        Space: O(1)

        The problem EXPLICITLY requires O(log n). This solution would be
        REJECTED in an interview because it ignores the sorted property
        of the input — wasted information.

        Kept here as the verbal baseline ("brute force is O(n) linear scan,
        but I'll use binary search for O(log n)") — not as a real submission.
        """
        for i, value in enumerate(nums):
            if value == target:
                return i
        return -1


# ============= TEST CASES =============
solution = Solution()

print(solution.search([-1, 0, 3, 5, 9, 12], 9))   # 4
print(solution.search([-1, 0, 3, 5, 9, 12], 2))   # -1
