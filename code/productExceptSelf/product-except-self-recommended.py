# Practice script: docs/exercise_scripts/LC238_ProductExceptSelf_practice.md

from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # answer[i] = (product of everything LEFT of i) * (product of everything RIGHT of i)
        #
        # Two passes:
        #   Pass 1 (left -> right): store the running product of items LEFT of i into result[i].
        #   Pass 2 (right -> left): multiply result[i] by the running product of items RIGHT of i.
        #
        # No division → handles zeros correctly.
        # O(1) extra space (the output array doesn't count by problem convention).

        n = len(nums)
        result = [1] * n

        # Pass 1 — left products
        left = 1
        for i in range(n):
            result[i] = left
            left *= nums[i]

        # Pass 2 — multiply in right products
        right = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right
            right *= nums[i]

        return result


# ============= TEST CASES =============
solution = Solution()

print(solution.productExceptSelf([1, 2, 3, 4]))         # [24, 12, 8, 6]
print(solution.productExceptSelf([-1, 1, 0, -3, 3]))    # [0, 0, 9, 0, 0]
print(solution.productExceptSelf([2, 3]))                # [3, 2]
print(solution.productExceptSelf([1, 1, 1, 1]))         # [1, 1, 1, 1]
print(solution.productExceptSelf([0, 0]))                # [0, 0]
