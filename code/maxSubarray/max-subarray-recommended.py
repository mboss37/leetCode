from typing import List

class Solution:
  def maxSubArray(self, nums: List[int]) -> int:
    
    max_global = max_current = nums[0]
    
    for num in nums[1:]:
            max_current = max(num, max_current + num)
            max_global = max(max_global, max_current)
        
    return max_global
        
nums = [2,-3,4,-2,2,1,-1,4]

solution = Solution()
result = solution.maxSubArray(nums)
print(result)