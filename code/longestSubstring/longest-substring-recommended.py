# Practice script: docs/exercise_scripts/LC3_LongestSubstring_practice.md

from typing import List


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Sliding window: L and R both move forward (no converging).
        # R walks every position exactly once. L lags behind, only advancing
        # when the window contains a duplicate.

        window = set()        # characters currently inside the window
        left = 0              # left edge of window
        best = 0              # longest valid window seen so far

        for right in range(len(s)):
            # Before adding s[right], make sure it's not already in the window.
            # If it is, shrink the window from the left until the duplicate is gone.
            while s[right] in window:
                window.remove(s[left])
                left += 1

            # Now safe to add the new character.
            window.add(s[right])

            # Window size is (right - left + 1). Update best.
            best = max(best, right - left + 1)

        return best


# ============= TEST CASES =============
solution = Solution()

print(solution.lengthOfLongestSubstring("abcabcbb"))   # 3 ("abc")
print(solution.lengthOfLongestSubstring("bbbbb"))      # 1 ("b")
print(solution.lengthOfLongestSubstring("pwwkew"))     # 3 ("wke")
print(solution.lengthOfLongestSubstring(""))           # 0
print(solution.lengthOfLongestSubstring("a"))          # 1
print(solution.lengthOfLongestSubstring("au"))         # 2
print(solution.lengthOfLongestSubstring("dvdf"))       # 3 ("vdf")
