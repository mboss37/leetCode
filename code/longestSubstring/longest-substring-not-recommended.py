# Practice script: docs/exercise_scripts/LC3_LongestSubstring_practice.md

from typing import List


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        BRUTE FORCE — try every starting position, extend until duplicate.

        Time:  O(n²)   — outer n, inner up to n
        Space: O(min(n, |alphabet|))

        At n = 50,000 (LC 3's max): 2.5 BILLION operations worst case. Too slow.
        The sliding-window optimal does it in O(n) by reusing the window.
        """
        n = len(s)
        longest = 0

        for i in range(n):
            seen = set()
            for j in range(i, n):
                if s[j] in seen:
                    break              # duplicate found — stop extending from i
                seen.add(s[j])
            longest = max(longest, len(seen))

        return longest


# ============= TEST CASES =============
solution = Solution()

print(solution.lengthOfLongestSubstring("abcabcbb"))   # 3
print(solution.lengthOfLongestSubstring("bbbbb"))      # 1
print(solution.lengthOfLongestSubstring("pwwkew"))     # 3
print(solution.lengthOfLongestSubstring(""))           # 0
