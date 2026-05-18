# Practice script: docs/exercise_scripts/LC153_FindMinInRotatedSortedArray_practice.md

from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        # Binary search variant. One half is always sorted; the min is in the
        # OTHER (unsorted) half — or at mid if it's the rotation pivot.

        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            # Compare mid to RIGHT (not left) to detect which half contains
            # the rotation pivot.
            if nums[mid] > nums[right]:
                # Left half is sorted, but min is somewhere AFTER mid.
                # Pivot (and min) live in the right half.
                left = mid + 1
            else:
                # Right half is sorted, min is in the left half OR is mid itself.
                # nums[mid] could BE the min; don't exclude it.
                right = mid

        # When left == right, we've narrowed to the min.
        return nums[left]


# ============= TEST CASES =============
solution = Solution()

print(solution.findMin([3, 4, 5, 1, 2]))          # 1
print(solution.findMin([4, 5, 6, 7, 0, 1, 2]))    # 0
print(solution.findMin([11, 13, 15, 17]))          # 11 — not rotated
print(solution.findMin([2, 1]))                    # 1
print(solution.findMin([1]))                       # 1 — single element
print(solution.findMin([5, 1, 2, 3, 4]))           # 1
