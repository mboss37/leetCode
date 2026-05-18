# Practice script: docs/exercise_scripts/LC128_LongestConsecutive_practice.md

from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # Put everything in a set for O(1) membership lookup.
        # Duplicates collapse automatically.
        s = set(nums)
        best = 0

        for num in s:
            # The "anchor check" — only START counting from the SMALLEST
            # element of a chain. If (num - 1) is in the set, num is
            # mid-chain and a smaller anchor will already count this run.
            if (num - 1) not in s:
                # num is the anchor — walk forward from here.
                current = num
                length = 1
                while (current + 1) in s:
                    current += 1
                    length += 1
                best = max(best, length)

        return best


# ============= TEST CASES =============
solution = Solution()

print(solution.longestConsecutive([100, 4, 200, 1, 3, 2]))         # 4  ([1,2,3,4])
print(solution.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])) # 9  ([0..8])
print(solution.longestConsecutive([]))                              # 0  (empty)
print(solution.longestConsecutive([1, 2, 0, 1]))                    # 3  ([0,1,2])
print(solution.longestConsecutive([2, 20, 4, 10, 3, 4, 5]))         # 4  ([2,3,4,5])
print(solution.longestConsecutive([1]))                             # 1  (single)
print(solution.longestConsecutive([1, 2, 3, 10, 11]))               # 3  ([1,2,3])
