# Practice script: docs/exercise_scripts/LC16_3SumClosest_practice.md

from typing import List


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        """
        BRUTE FORCE — three nested loops.

        Time:  O(n³)
        Space: O(1)

        At n=500 (LC 16's max): ~21M operations. Borderline acceptable.
        Use the recommended solution for fluency.
        """
        n = len(nums)
        closest_sum = nums[0] + nums[1] + nums[2]  # baseline from first three

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    current_sum = nums[i] + nums[j] + nums[k]
                    if abs(current_sum - target) < abs(closest_sum - target):
                        closest_sum = current_sum

        return closest_sum


# ============= TEST CASES =============
solution = Solution()

print(solution.threeSumClosest([-1, 2, 1, -4], 1))             # 2
print(solution.threeSumClosest([0, 0, 0], 1))                  # 0
print(solution.threeSumClosest([1, 1, 1, 0], -100))            # 2
