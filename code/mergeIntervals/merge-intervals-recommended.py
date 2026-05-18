# Practice script: docs/exercise_scripts/LC56_MergeIntervals_practice.md

from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Sort by start time so overlapping intervals become ADJACENT.
        # Once sorted, a single sweep can merge them.
        intervals.sort(key=lambda x: x[0])

        merged = []
        for current in intervals:
            # If merged is empty OR current doesn't overlap the last → append new.
            # If current.start ≤ last.end → they overlap, extend last.end.
            if not merged or current[0] > merged[-1][1]:
                merged.append(current)
            else:
                # Overlap → extend the END of the last merged interval.
                merged[-1][1] = max(merged[-1][1], current[1])

        return merged


# ============= TEST CASES =============
solution = Solution()

print(solution.merge([[1, 3], [2, 6], [8, 10], [15, 18]]))   # [[1,6],[8,10],[15,18]]
print(solution.merge([[1, 4], [4, 5]]))                       # [[1,5]] — touching counts
print(solution.merge([[1, 4]]))                               # [[1,4]] — single interval
print(solution.merge([[1, 4], [0, 4]]))                       # [[0,4]] — out-of-order input
print(solution.merge([[1, 4], [2, 3]]))                       # [[1,4]] — second nested inside first
print(solution.merge([[1, 10], [2, 3], [4, 5], [6, 7]]))      # [[1,10]] — all nested
