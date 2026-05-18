class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = ''.join(c.lower() for c in s if c.isalnum())
        return cleaned == cleaned[::-1]

s = "Was it a car or a cat I saw?"

solution = Solution()
result = solution.isPalindrome(s)
print(result)