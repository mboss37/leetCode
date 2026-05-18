from typing import List

class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
      seen = set() # Store the value only
      
      for num in nums:
        seen.add(num)
        if len(seen) < len(nums): 
          return True
      return False
      
nums = [1,2,3,3]

solution = Solution()
result = solution.hasDuplicate(nums)

print(result)