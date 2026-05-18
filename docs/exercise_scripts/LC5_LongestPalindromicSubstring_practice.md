# LC 5 — Longest Palindromic Substring · Practice Script

**Code:** [code/longestPalindromicSubstring/](../../code/longestPalindromicSubstring/)

---

## Problem

> Given a string `s`, return the **longest palindromic substring** in `s`. A palindrome reads the same forwards and backwards.

**Constraints:**
- `1 <= s.length <= 1000`
- `s` contains only digits and English letters.

---

## RECOMMENDED — Expand Around Center (O(n²))

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""
        start, max_len = 0, 1

        def expand(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return left + 1, right - left - 1   # start, length

        for i in range(len(s)):
            s1, l1 = expand(i, i)        # odd-length center
            s2, l2 = expand(i, i + 1)    # even-length center
            if l1 > max_len:
                start, max_len = s1, l1
            if l2 > max_len:
                start, max_len = s2, l2

        return s[start:start + max_len]
```

### The key idea

**Every palindrome has a center.** Two cases:

1. **Odd length** (e.g. `"aba"`) — center is a single char.
2. **Even length** (e.g. `"abba"`) — center is BETWEEN two chars.

For a string of length `n`, there are `2n - 1` possible centers: `n` single-char centers + `n - 1` between-char centers.

For each center, **expand outward** as long as the characters on both sides match. Track the longest expansion seen.

### Trace on `s = "babad"`

| i | odd expand | length | even expand | length | best so far |
|---|---|---|---|---|---|
| 0 | "b" | 1 | "" (b≠a) | 0 | "b" (1) |
| 1 | "bab" | 3 | "" (a≠b) | 0 | "bab" (3) |
| 2 | "aba" | 3 | "" (b≠a) | 0 | "bab" or "aba" (3) |
| 3 | "a" | 1 | "" | 0 | (3) |
| 4 | "d" | 1 | — | — | (3) |

Result: `"bab"` (or `"aba"` — both are valid). ✓

### Why it's correct

We try EVERY possible center. The longest palindromic substring must have SOME center, and expansion from that center captures it fully.

### Complexity

- **Time:** O(n²) — each of `2n - 1` centers expands at most `n` times
- **Space:** O(1) — just two index/length scalars

n ≤ 1000 → 10⁶ ops, trivially fast.

---

## Alternative — DP (O(n²) time, O(n²) space)

```python
class Solution:
    def longestPalindrome(self, s):
        n = len(s)
        dp = [[False]*n for _ in range(n)]
        start, max_len = 0, 1
        for i in range(n): dp[i][i] = True
        for i in range(n-1):
            if s[i] == s[i+1]:
                dp[i][i+1] = True
                start, max_len = i, 2
        for length in range(3, n+1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and dp[i+1][j-1]:
                    dp[i][j] = True
                    if length > max_len:
                        start, max_len = i, length
        return s[start:start+max_len]
```

`dp[i][j]` = is `s[i..j]` a palindrome? Build up by length. Same big-O as expand-around-center, but O(n²) space. **Expand-around-center wins on space.**

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting the even-length case | Misses "abba"-style palindromes | Two expand calls per `i`: (i,i) AND (i,i+1) |
| Returning indices instead of substring | Wrong return type | `s[start:start + max_len]` |
| Off-by-one on `expand` return | Length wrong by 2 | `length = right - left - 1` (the loop overshoots by one on each side) |
| Comparing chars only at the edges | Misses inner mismatches | The `while ... s[left] == s[right]` handles each step |
| Initializing max_len = 0 | Returns empty string for non-empty input | `max_len = 1` so single chars always count |

---

## Marker — Manacher's Algorithm (O(n))

There IS an O(n) solution called **Manacher's algorithm**. It's clever but tricky and rarely expected in a 45-minute interview. **Don't memorize it.** If pushed, say:
> "I know Manacher's algorithm gets this to O(n) by reusing palindrome info from previous centers — happy to walk through it, but expand-around-center O(n²) is fast enough for n ≤ 1000 here."

---

## Interview Out-Loud

> "Every palindrome has a center. For odd-length palindromes the center is a single character; for even-length it's between two characters. 2n - 1 possible centers total.
>
> For each center, expand outward while the two sides match. Track the longest expansion seen.
>
> O(n²) time — n centers, up to n expansion steps each. O(1) space.
>
> If interviewer pushes for O(n), I'd mention Manacher's algorithm but skip the implementation unless required."

---

**Chain position:** Center-expansion pattern. Related: Palindromic Substrings (count), Longest Palindromic Subsequence (DP, different problem).
