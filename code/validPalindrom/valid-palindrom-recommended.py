class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1

        # Skip non-alphanumeric characters from left
        while left < right:                                 # Main loop: keep going until pointers meet
            while left < right and not s[left].isalnum():   # Move left pointer forward until we find a valid character
                left += 1                                   

            # Skip non-alphanumeric characters from right
            while left < right and not s[right].isalnum():
                right -= 1

            # Compare characters (case-insensitive)
            if s[left].lower() != s[right].lower():
                return False
        
            left +=1
            right -=1
        
        return True


s = "Was it a car or a cat I saw?"

solution = Solution()
result = solution.isPalindrome(s)
print(result)