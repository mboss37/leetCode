from typing import List


class Solution:
    def threeSum(self, numbers: List[int]) -> List[List[int]]:
        # Sort first. Two reasons:
        #   1. Enables two-pointer reasoning (sorted means moving L right raises the
        #      sum, moving R left lowers it — no backtracking needed).
        #   2. Groups duplicate values next to each other, so the three skip-checks
        #      below only need to look at the immediate neighbor.
        # Using sorted() (not .sort()) so we don't mutate the caller's input.
        # Cost: O(n) extra space. Trivial for LC 15's n <= 3000.
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        result = []

        # Outer "anchor" loop. Walk i from 0 to n-3 inclusive — we need at least
        # two positions to the right of i (for L and R).
        for i in range(n - 2):
            # ----- SKIP 1: duplicate anchors -----
            # If this anchor's VALUE equals the previous anchor's VALUE, every
            # triplet we'd find here was already found by the previous anchor.
            # The `i > 0` guard prevents looking at sorted_nums[-1], which in
            # Python is the LAST element (silent bug without the guard).
            if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
                continue

            # Reset pointers for this anchor. MUST live inside the outer loop —
            # if defined outside, the second anchor starts with stale pointers.
            left, right = i + 1, n - 1

            while left < right:
                current_sum = sorted_nums[i] + sorted_nums[left] + sorted_nums[right]

                if current_sum == 0:
                    # Match — record the triplet (as a fresh list).
                    result.append([sorted_nums[i], sorted_nums[left], sorted_nums[right]])

                    # ----- SKIP 2: duplicate L values -----
                    # Walk L past any neighbors holding the same value as L just had.
                    # Otherwise the same triplet would reappear in the next iteration.
                    while left < right and sorted_nums[left] == sorted_nums[left + 1]:
                        left += 1

                    # ----- SKIP 3: duplicate R values -----
                    # Walk R past any neighbors holding the same value as R just had.
                    while left < right and sorted_nums[right] == sorted_nums[right - 1]:
                        right -= 1

                    # Now step one more — onto FRESH values that weren't in the
                    # triplet we just recorded.
                    left += 1
                    right -= 1

                elif current_sum < 0:
                    # Sum too small → bump L right to bring in a bigger number.
                    left += 1
                else:
                    # Sum too big → bump R left to bring in a smaller number.
                    right -= 1

        return result


# ============= TEST CASES =============
solution = Solution()

print(solution.threeSum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
print(solution.threeSum([0, 0, 0]))              # [[0, 0, 0]]
print(solution.threeSum([0, 0, 0, 0]))           # [[0, 0, 0]]  — dedup test
print(solution.threeSum([1, 2, 3]))              # []           — no triplet sums to 0
print(solution.threeSum([]))                     # []           — empty
print(solution.threeSum([-2, 0, 1, 1, 2]))       # [[-2, 0, 2], [-2, 1, 1]]
print(solution.threeSum([3, 0, -2, -1, 1, 2]))   # [[-2, -1, 3], [-2, 0, 2], [-1, 0, 1]]
