# Practice script: docs/exercise_scripts/LC34_FindFirstAndLastPosition_practice.md

from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # Two separate binary searches — one biased LEFT, one biased RIGHT.
        # Each is plain Binary Search with one tweak: on a match, record
        # the index but KEEP NARROWING in the biased direction to look for
        # an even better occurrence.

        def find_left(nums, target):
            # Find the LEFTMOST index where nums[i] == target, or -1 if not found.
            left, right = 0, len(nums) - 1
            result = -1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] == target:
                    result = mid          # record this hit
                    right = mid - 1       # keep looking LEFT for an earlier match
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return result

        def find_right(nums, target):
            # Find the RIGHTMOST index where nums[i] == target, or -1 if not found.
            left, right = 0, len(nums) - 1
            result = -1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] == target:
                    result = mid          # record this hit
                    left = mid + 1        # keep looking RIGHT for a later match
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return result

        return [find_left(nums, target), find_right(nums, target)]


# ============= TEST CASES =============
sol = Solution()

print(sol.searchRange([5, 7, 7, 8, 8, 10], 8))     # [3, 4]
print(sol.searchRange([5, 7, 7, 8, 8, 10], 6))     # [-1, -1]
print(sol.searchRange([], 0))                       # [-1, -1]
print(sol.searchRange([1], 1))                      # [0, 0]
print(sol.searchRange([1], 0))                      # [-1, -1]
print(sol.searchRange([2, 2], 2))                   # [0, 1]
print(sol.searchRange([1, 2, 3, 3, 3, 3, 3, 4, 5], 3))   # [2, 6]
