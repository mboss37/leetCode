# Practice script: docs/exercise_scripts/LC704_BinarySearch_practice.md

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # Binary search on a sorted array. Halve the search range each step.
        # Two indices mark the current search window: [left, right] inclusive.

        left = 0
        right = len(nums) - 1

        # `<=` (not `<`) — when left == right there's still ONE element to check.
        # Using `<` would skip that final element. Off-by-one trap.
        while left <= right:
            # Integer division for the middle index.
            # In Java/C++ this can overflow on huge n; the safer expression is
            # `left + (right - left) // 2`. In Python ints are unbounded, so
            # the simpler form is fine.
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                # Target must be in the right half. mid is already checked
                # (it wasn't equal), so exclude it: left = mid + 1.
                left = mid + 1
            else:
                # Target must be in the left half.
                right = mid - 1

        # left has crossed right. Target doesn't exist in nums.
        return -1


# ============= TEST CASES =============
solution = Solution()

print(solution.search([-1, 0, 3, 5, 9, 12], 9))   # 4
print(solution.search([-1, 0, 3, 5, 9, 12], 2))   # -1
print(solution.search([5], 5))                    # 0   — single element, hit
print(solution.search([5], 1))                    # -1  — single element, miss
print(solution.search([1, 2, 3, 4, 5], 1))        # 0   — first element
print(solution.search([1, 2, 3, 4, 5], 5))        # 4   — last element
print(solution.search([], 1))                     # -1  — empty (spec says n >= 1, but defensive)
