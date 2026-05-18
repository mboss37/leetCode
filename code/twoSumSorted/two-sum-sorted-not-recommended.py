from typing import List

class Solution:
  def twoSum(self, numbers: List[int], target: int) -> List[int]:
    
    for i in range(len(numbers)):
      for j in range(i + 1, len(numbers)):
        current_sum = numbers[i] + numbers[j]
        if current_sum == target:
          return [i + 1, j + 1]
    return []
          
    
numbers = [1,2,3,4]
target = 3
solution = Solution()

result = solution.twoSum(numbers, target)
print(result)