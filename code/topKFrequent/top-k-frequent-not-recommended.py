# Practice script: docs/exercise_scripts/LC347_TopKFrequent_practice.md
#
# This is the "without most_common" follow-up version.
# Lead with the Counter.most_common(k) approach (top-k-frequent-recommended.py).
# Only write this if the interviewer explicitly says:
#     "Now do it without using most_common."

import heapq
from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Manual min-heap of size K.

        Same O(n log k) time as Counter.most_common (which uses this internally).
        Demonstrates the algorithm explicitly.
        """
        # Step 1: count frequencies — O(n)
        counts = Counter(nums)

        # Step 2: build a min-heap of size k.
        # Heap entries are (count, number) tuples so heapq compares by count.
        # Keep only the k LARGEST counts. Pop the smallest when size > k.
        heap = []
        for num, count in counts.items():
            heapq.heappush(heap, (count, num))
            if len(heap) > k:
                heapq.heappop(heap)
        # After the loop, the heap holds the k most-frequent (number, count) pairs.

        # Step 3: extract just the numbers.
        # Order doesn't matter per the spec.
        result = []
        for count, num in heap:
            result.append(num)
        return result


# ============= TEST CASES =============
solution = Solution()

print(solution.topKFrequent([1, 1, 1, 2, 2, 3], 2))         # [1, 2] in any order
print(solution.topKFrequent([1], 1))                         # [1]
print(solution.topKFrequent([1, 2, 2, 3, 3, 3], 3))         # [1, 2, 3] in any order
print(solution.topKFrequent([4, 4, 4, 4, 5, 5, 6], 1))      # [4]
