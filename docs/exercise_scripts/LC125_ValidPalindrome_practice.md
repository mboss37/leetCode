# LC 125 — Valid Palindrome · Practice Script

**Problem:**  
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.  
Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

---

## Solution 1: Brute Force (Clean + Reverse)

```python
from typing import List

class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = ''.join(c.lower() for c in s if c.isalnum())
        return cleaned == cleaned[::-1]
```

### Why this is NOT recommended as the main solution

- Creates a new string (`cleaned`) → extra O(n) space
- Uses slicing `cleaned[::-1]` which is O(n) time
- Less elegant — doesn’t demonstrate the **two-pointer pattern** (very common in medium problems)
- Interviewers prefer solutions that show you can solve it **in-place** with O(1) extra space

---

## Solution 2: Optimal Two Pointers (Recommended)

```python
from typing import List

class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        
        while left < right:
            # Skip non-alphanumeric characters from left
            while left < right and not s[left].isalnum():
                left += 1
            
            # Skip non-alphanumeric characters from right
            while left < right and not s[right].isalnum():
                right -= 1
            
            # Compare characters (case-insensitive)
            if s[left].lower() != s[right].lower():
                return False
            
            left += 1
            right -= 1
        
        return True
```

### Why this is RECOMMENDED

- **Time Complexity:** O(n) — single pass with two pointers
- **Space Complexity:** O(1) — no extra string created
- Demonstrates the **two-pointer technique** (critical pattern for many medium problems)
- More efficient and professional
- Shows you can handle edge cases (skipping non-alphanumeric characters) cleanly

---

## Comparison Table

| Aspect                  | Brute Force (Sorting/Reverse)      | Two Pointers (Recommended)      | Winner      |
|-------------------------|------------------------------------|----------------------------------|-------------|
| Time Complexity         | O(n)                               | O(n)                             | Tie         |
| Space Complexity        | O(n) (new string)                  | **O(1)**                         | Two Pointers|
| Code cleanliness        | Very short                         | Slightly longer but clearer      | Two Pointers|
| Shows problem-solving   | Basic                              | **Strong** (two-pointer pattern) | Two Pointers|
| Interview signal        | Acceptable                         | **Strongly preferred**           | Two Pointers|

---

## Key Points

- Always check for **non-alphanumeric** characters — this is the main gotcha.
- Use `.isalnum()` and `.lower()` — very useful in Python.
- Two-pointer technique from both ends is a classic pattern (you will see it again in problems like Container With Most Water, 3Sum, etc.).
- You can solve it **in-place** without creating extra strings.

---

## Test Cases

| Input                                      | Expected | Notes |
|--------------------------------------------|----------|-------|
| `"A man, a plan, a canal: Panama"`         | `true`   | Classic example |
| `"race a car"`                             | `false`  | — |
| `" "`                                      | `true`   | Empty after cleaning |
| `"0P"`                                     | `false`  | Different characters |
| `"Madam"`                                  | `true`   | Case insensitive |
| `"No lemon, no melon"`                     | `true`   | — |

---

## Interview Out-Loud

> "For Valid Palindrome, the brute force way is to clean the string by removing non-alphanumeric characters and converting to lowercase, then check if it equals its reverse. That works but creates an extra string and uses O(n) space.
>
> A better approach is to use **two pointers** — one starting from the left and one from the right. We move them toward the center, skipping any non-alphanumeric characters, and compare the characters (case-insensitive). If we find a mismatch, we return false. If the pointers meet or cross, the string is a palindrome.
>
> This solution runs in O(n) time and uses O(1) extra space. It also demonstrates the two-pointer pattern, which is very useful for many other problems."

---

## Recommended Daily Practice Flow (for this problem)

1. Write the **two-pointer version** from memory (no looking)
2. Talk out loud while writing (record yourself once)
3. Write 5–6 test cases yourself
4. Retape the solution the next day from memory
5. Be ready to explain why two pointers is better than creating a new string

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting to skip non-alphanumeric inside the loop | `' '` and `'A'` would compare directly | `while not s[left].isalnum(): left += 1` (and same for right) |
| Not lowercasing | `'A'` and `'a'` are different characters | Compare `s[left].lower() == s[right].lower()` |
| `while left <= right` | Compares the middle char to itself — harmless but unnecessary | Use `left < right` |
| Skipping past `right` boundary | If you skip too eagerly, `left` can pass `right` mid-skip | Add `left < right` guard INSIDE the skip-while loops |
| Reaching for `s[::-1] == s` when interviewer wants O(1) space | O(n) extra space for the reversed string | State that approach verbally, write the two-pointer version |

---

## Chain position

Valid Palindrome is the **converging two-pointer on string** pattern. The "meet in the middle" idea extends to:
- **Valid Palindrome II** — same skeleton, but allow one character deletion
- **Reverse String / Reverse Vowels** — same converging pattern, different action per step
- **Longest Palindromic Substring** — expand-around-center (related but different)
- **Two Sum Sorted** — same converging two-pointer on numbers instead of characters

Master the "two pointers from both ends, skip irrelevant, meet in middle" reflex — it's the simplest two-pointer variant and shows up in 5+ problems.