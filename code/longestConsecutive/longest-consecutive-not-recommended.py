# Practice script: docs/exercise_scripts/LC128_LongestConsecutive_practice.md
#
# NOT the version to lead with — spec demands O(n).
# Lead with the set + anchor version (longest-consecutive-recommended.py).
# This sort + sweep approach is O(n log n), which would be REJECTED by the
# strict spec. Kept here only as the verbal comparison baseline.

from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """
        SORT + SWEEP — NOT RECOMMENDED.

        Time:  O(n log n) — sorting dominates
        Space: O(n) — sorted() creates a new list

        Spec requires O(n). In an interview, state this verbally as the
        naive baseline ("Sort then walk, O(n log n) — but spec wants O(n)")
        and write the set + anchor version instead.

        Trade-off: this version doesn't need the "anchor" insight, so it's
        easier to reason about — but it doesn't meet the spec.
        """
        if not nums:
            return 0

        # Dedupe via set + sort. Duplicates create gap=0 — easier to drop
        # them upfront than handle gap==0 in the loop logic.
        sorted_arr = sorted(set(nums))

        best = 1
        current = 1

        for i in range(1, len(sorted_arr)):
            if sorted_arr[i] - sorted_arr[i - 1] == 1:
                # Consecutive — extend the current run.
                current += 1
                best = max(best, current)
            else:
                # Gap broke the run — reset.
                current = 1

        return best


# ============= TEST CASES =============
solution = Solution()

print(solution.longestConsecutive([100, 4, 200, 1, 3, 2]))         # 4
print(solution.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])) # 9
print(solution.longestConsecutive([]))                              # 0
print(solution.longestConsecutive([1, 2, 0, 1]))                    # 3
print(solution.longestConsecutive([1, 2, 3, 10, 11]))               # 3
