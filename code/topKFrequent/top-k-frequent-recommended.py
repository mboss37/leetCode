# Practice script: docs/exercise_scripts/LC347_TopKFrequent_practice.md

from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Count frequencies — Counter is built for this.
        counts = Counter(nums)

        # most_common(k) returns the k most-frequent items as a list of
        # (number, count) tuples, already sorted by frequency.
        # Internally it uses a min-heap of size k → O(n log k).
        top_pairs = counts.most_common(k)

        # Extract just the numbers (drop the counts).
        result = []
        for num, count in top_pairs:
            result.append(num)
        return result


# ============= TEST CASES =============
solution = Solution()

print(solution.topKFrequent([1, 1, 1, 2, 2, 3], 2))         # [1, 2]
print(solution.topKFrequent([1], 1))                         # [1]
print(solution.topKFrequent([1, 2, 2, 3, 3, 3], 3))         # [3, 2, 1]
print(solution.topKFrequent([4, 4, 4, 4, 5, 5, 6], 1))      # [4]
print(solution.topKFrequent([1, 1, 2, 2, 3, 3], 2))         # any 2 of [1, 2, 3]
