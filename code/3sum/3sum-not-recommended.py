from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        BRUTE FORCE — three nested loops.

        Time:  O(n³)   — try every triple of positions.
        Space: O(k)    — k = number of unique value-triplets, stored in the set.

        At n=500 (LC 15's max): ~125M operations. Borderline.
        At n=3000:              ~27B operations. Way too slow.

        Use the recommended solution for production / interviews. This file
        exists only as the "what you'd write without the sort + two-pointer trick"
        baseline that an interviewer expects you to STATE before optimizing.
        """
        n = len(nums)
        final_list = set()  # Set of sorted tuples — auto-dedupes value-level duplicates.

        # Enforce i < j < k via range(i+1, n) and range(j+1, n) on the inner loops.
        # Without that, we'd visit (0,1,2), (0,2,1), (1,0,2), ... — same combo,
        # different orderings, n³ work instead of n³/6.
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        # Sort the triplet so [-1, 0, 1] and [0, 1, -1] become the
                        # same tuple key. Tuple (not list) because sets only accept
                        # IMMUTABLE items — lists are mutable, sets reject them.
                        triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                        final_list.add(triplet)

        # Convert back to list of lists for the expected output format.
        return [list(t) for t in final_list]


# ============= TEST CASES =============
solution = Solution()

print(solution.threeSum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
print(solution.threeSum([0, 0, 0]))              # [[0, 0, 0]]
print(solution.threeSum([1, 2, 3]))              # []
