# Practice script: docs/exercise_scripts/LC20_ValidParentheses_practice.md

class Solution:
    def isValid(self, s: str) -> bool:
        # Stack pattern — LIFO matches the bracket nesting rule.
        # "Last opened, first closed."

        # Dict: closer → expected opener. Closers are the keys; we look up
        # whichever closer we see and check it against the stack's top.
        pairs = {")": "(", "]": "[", "}": "{"}

        stack = []  # holds OPENERS we've seen but haven't matched yet

        for c in s:
            if c in pairs:
                # c is a closer. Two ways it can be invalid:
                #   1. Stack is empty — no opener to match against.
                #   2. Top of stack isn't the matching opener.
                if not stack or stack.pop() != pairs[c]:
                    return False
            else:
                # c is an opener. Push and continue.
                stack.append(c)

        # If anything is left on the stack, openers went unmatched.
        return not stack


# ============= TEST CASES =============
solution = Solution()

print(solution.isValid("()"))            # True
print(solution.isValid("()[]{}"))        # True
print(solution.isValid("(]"))            # False — wrong type
print(solution.isValid("([)]"))          # False — cross-nested
print(solution.isValid("{[]}"))          # True  — properly nested
print(solution.isValid(""))              # True  — empty is vacuously valid
print(solution.isValid("("))             # False — unmatched opener
print(solution.isValid(")"))             # False — closer with no opener
print(solution.isValid("()[]{})"))       # False — extra closer at end
