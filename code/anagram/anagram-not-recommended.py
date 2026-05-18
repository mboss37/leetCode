from typing import List

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        return sorted(s) == sorted(t)

s = "racecar"
t = "carrace"

solution = Solution()
result = solution.isAnagram(s, t)
print(result)
