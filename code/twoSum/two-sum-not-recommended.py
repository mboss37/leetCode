from typing import List   ## List must be imported for type hints


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):                    # outer loop. i = 0, 1, 2, 3
            for j in range(i + 1, len(nums)):         # inner loop starts after i. (3+4),(3+5),(3+6)
                if nums[i] + nums[j] == target:
                    return [i, j]
        
        return []                                     # no solution found
# ====================== NOTES FOR LEARNING ======================
# Time Complexity: O(n²)
# Formula for inner loop iterations: n(n-1)/2
# Example with n=5: 5×4/2 = 10 comparisons
# This is why brute force becomes slow for large arrays.


# ====================== TESTING THE CODE ======================

# Test data
nums = [3, 4, 5, 6]      # This is our input list
target = 7               # We are looking for two numbers that sum to 7

# Step 1: Create an object (instance) of the Solution class
solution = Solution()

# Step 2: Call the twoSum method using the object
# We pass nums and target as arguments
result = solution.twoSum(nums, target)

# Step 3: Print the result so we can see the answer
print(result)            # Expected output: [0, 1] because 3 + 4 = 7