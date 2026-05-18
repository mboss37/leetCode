# Practice script: docs/exercise_scripts/LC20_ValidParentheses_practice.md

class Solution:
    def isValid(self, s: str) -> bool:
        """
        BRUTE FORCE — repeated pair removal.

        Time:  O(n²)
        Space: O(n)

        Each .replace() is O(n) (creates a new string). Outer loop runs up to
        n/2 times. At n=10000 (LC 20's max): ~50M ops. Accepted by judge but
        ~5000x slower than the stack version. Hides the LIFO insight.
        Rejected in interview because it doesn't show algorithmic thinking.
        """
        # Repeatedly strip any complete matched pair. Whatever survives the
        # peeling-off either:
        #   - Reduces to empty → string was valid.
        #   - Stays non-empty (unmatched brackets) → invalid.
        while '()' in s or '[]' in s or '{}' in s:
            s = s.replace('()', '').replace('[]', '').replace('{}', '')

        return s == ''


# ============= TEST CASES =============
solution = Solution()

print(solution.isValid("()"))            # True
print(solution.isValid("()[]{}"))        # True
print(solution.isValid("(]"))            # False
print(solution.isValid("([)]"))          # False — cross-nested can't be peeled
print(solution.isValid("{[]}"))          # True
print(solution.isValid(""))              # True
print(solution.isValid("()[]{})"))       # False
