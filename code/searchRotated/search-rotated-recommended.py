# Practice script: docs/exercise_scripts/LC33_SearchInRotatedSortedArray_practice.md

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # Binary search variant. At every step, one half is guaranteed sorted.
        # Figure out which half is sorted, then check if target lies in it.

        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            # Left half [left..mid] is sorted iff nums[left] <= nums[mid]
            if nums[left] <= nums[mid]:
                # Target in the sorted left half?
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                # Right half [mid..right] is sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1


# ============= TEST CASES =============
solution = Solution()

print(solution.search([4, 5, 6, 7, 0, 1, 2], 0))     # 4
print(solution.search([4, 5, 6, 7, 0, 1, 2], 3))     # -1
print(solution.search([1], 0))                        # -1
print(solution.search([1, 3], 3))                     # 1
print(solution.search([5, 1, 3], 5))                  # 0
print(solution.search([6, 7, 0, 1, 2, 4, 5], 2))     # 4
