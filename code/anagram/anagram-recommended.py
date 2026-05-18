from typing import List

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        seen = {}
        
        for char in s:
            seen[char] = seen.get(char, 0) + 1  # store char in hashmap with count
            
        for char in t:
            if char not in seen:              
                return False                    # stop loop and return false. No anagram
            seen[char] -= 1                     # reduce count of char in hashmap by one
            if seen[char] == 0:                 
                del seen[char]                  # if char count is 0, remove from hashmap
        
        return len(seen) == 0                   # if hashmap is emtpy, we got the anagram. return True
                
                
s = "racecar"
t = "carrace"

solution = Solution()
result = solution.isAnagram(s, t)
print(result)
