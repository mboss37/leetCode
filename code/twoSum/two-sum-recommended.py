from typing import List   ## List must be imported for type hints

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}                              # hashmap: value -> index

        for i, num in enumerate(nums):
            complement = target - num          # what we still need to reach the target

            if complement in seen:
                return [seen[complement], i]   # found the pair!

            seen[num] = i                      # store current value + its index

        return []                              # no solution found
    
    
# ====================== TESTING THE CODE ======================

# Test data
nums = [2,7,4,6,9]
target = 8

# Step 1: Create an object (instance) of the Solution class
solution = Solution()

# Step 2: Call the twoSum method using the object
# We pass nums and target as arguments
result = solution.twoSum(nums, target)

# Step 3: Print the result so we can see the answer
print(result)            # Expected output: [0, 3] because 2 + 6 = 8

# First iteration (i = 0, num = 2):

# complement = 8 - 2 = 6
# Is 6 in seen? → No
# We store the current number: seen[2] = 0
# Now seen = {2: 0}

# Second iteration (i = 1, num = 7):

# complement = 8 - 7 = 1
# Not in seen → store seen[7] = 1

# Third iteration (i = 2, num = 4):

# complement = 8 - 4 = 4
# Not in seen → store seen[4] = 2

# Fourth iteration (i = 3, num = 6):

# complement = 8 - 6 = 2
# 2 is in seen → return [0, 3]