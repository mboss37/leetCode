# Practice script: docs/exercise_scripts/LC16_3SumClosest_practice.md

from typing import List


class Solution:
    def threeSumClosest(self, numbers: List[int], target: int) -> int:
        # Sort to enable two-pointer reasoning.
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)

        # Initialize tracker to a real triplet sum so the first comparison is meaningful.
        closest_sum = sorted_nums[0] + sorted_nums[1] + sorted_nums[2]

        for i in range(n - 2):
            left = i + 1
            right = n - 1

            while left < right:
                current_sum = sorted_nums[i] + sorted_nums[left] + sorted_nums[right]

                # Update the tracker if this sum is closer to target (smaller absolute distance).
                if abs(current_sum - target) < abs(closest_sum - target):
                    closest_sum = current_sum

                # Three-branch direction logic — same as LC 167 / LC 15.
                if current_sum < target:
                    left += 1
                elif current_sum > target:
                    right -= 1
                else:
                    # Distance 0. Unbeatable. Return immediately.
                    return target

        return closest_sum


# ============= TEST CASES =============
solution = Solution()

print(solution.threeSumClosest([-1, 2, 1, -4], 1))             # 2
print(solution.threeSumClosest([0, 0, 0], 1))                  # 0
print(solution.threeSumClosest([1, 1, 1, 0], -100))            # 2
print(solution.threeSumClosest([-1, 0, 1, 2, -1, -4], 5))      # 3
print(solution.threeSumClosest([-3, -2, -5, 3, -4], -1))       # -2
