# Practice script: docs/exercise_scripts/LC35_SearchInsertPosition_practice.md

from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        # Binary search variant. Same skeleton as plain Binary Search —
        # the ONLY change is the final return: `left` instead of -1.
        #
        # When the loop exits without finding the target, `left` points to
        # where target should be inserted to keep the array sorted.

        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        # Why `left` works as the insertion position:
        #   When the loop exits, left > right.
        #   `left` has been advanced past every index where nums[idx] < target,
        #   and `right` has been pulled before every index where nums[idx] > target.
        #   The "hole" between them — at index `left` — is exactly where target belongs.
        return left


# ============= TEST CASES =============
solution = Solution()

print(solution.searchInsert([1, 3, 5, 6], 5))   # 2  — exact match
print(solution.searchInsert([1, 3, 5, 6], 2))   # 1  — insert between 1 and 3
print(solution.searchInsert([1, 3, 5, 6], 7))   # 4  — insert at end
print(solution.searchInsert([1, 3, 5, 6], 0))   # 0  — insert at start
print(solution.searchInsert([1], 0))            # 0  — single element, insert before
print(solution.searchInsert([1], 2))            # 1  — single element, insert after
print(solution.searchInsert([1, 3], 3))         # 1  — match at end
