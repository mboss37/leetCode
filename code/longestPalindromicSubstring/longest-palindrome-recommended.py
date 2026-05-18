# Practice script: docs/exercise_scripts/LC5_LongestPalindromicSubstring_practice.md


class Solution:
    def longestPalindrome(self, s: str) -> str:
        # Every palindrome has a center. There are 2n-1 possible centers:
        #   n single-char centers (odd-length palindromes)
        #   n-1 between-char centers (even-length palindromes)
        #
        # For each center, expand outwards while characters match.
        # Track the longest expansion seen.

        if not s:
            return ""

        start, max_len = 0, 1   # at minimum, a single char is a palindrome

        def expand(left: int, right: int) -> tuple[int, int]:
            """Expand around (left, right) while in bounds and matching.
            Returns (start_index, length) of the maximal palindrome found."""
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # Loop ended one step past the valid range — adjust.
            return left + 1, right - left - 1

        for i in range(len(s)):
            # Odd length — single-char center.
            s1, l1 = expand(i, i)
            # Even length — between-char center.
            s2, l2 = expand(i, i + 1)
            if l1 > max_len:
                start, max_len = s1, l1
            if l2 > max_len:
                start, max_len = s2, l2

        return s[start : start + max_len]


# ============= TEST CASES =============
solution = Solution()

print(solution.longestPalindrome("babad"))       # "bab" or "aba"
print(solution.longestPalindrome("cbbd"))        # "bb"
print(solution.longestPalindrome("a"))           # "a"
print(solution.longestPalindrome("ac"))          # "a" or "c"
print(solution.longestPalindrome("racecar"))     # "racecar"
print(solution.longestPalindrome("abacdfgdcaba")) # "aba" or "aca"
print(solution.longestPalindrome(""))             # ""
