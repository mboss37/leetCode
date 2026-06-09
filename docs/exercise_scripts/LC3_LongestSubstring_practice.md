# LC 3 — Longest Substring Without Repeating Characters · Practice Script

---

## Problem

> Given a string `s`, find the **length** of the **longest substring** without repeating characters.

**Constraints:**
- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols, and spaces.

**Key word:** *substring* = **contiguous** slice (not a subsequence). `"abc"` is a substring of `"axbxc"` only if it appears consecutively, which it doesn't.

Output: a single integer (the length).

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Substring means contiguous, right — not a subsequence?"** — Yes, contiguous. A subsequence version is a completely different problem.
- **"What characters can appear — lowercase only, or any ASCII?"** — Letters, digits, symbols, spaces. So a set works; a fixed 26-slot array does not.
- **"Can the string be empty, and what do I return then?"** — Yes, length can be 0. Return 0.
- **"Do you want just the length, or the substring itself?"** — Just the length. Returning the string means tracking the best window's start index too.
- **"Is 'A' different from 'a'?"** — Assume case-sensitive unless told otherwise.

---

## 1. Brute Force (O(n²))

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        longest = 0

        for i in range(n):
            seen = set()
            for j in range(i, n):
                if s[j] in seen:
                    break              # duplicate — stop extending from i
                seen.add(s[j])
            longest = max(longest, len(seen))

        return longest
```

- **Time:** O(n²) — outer pick of start, inner extend until duplicate.
- **Space:** O(min(n, |alphabet|)).
- **Wasteful** because when a duplicate is found, the entire substring is thrown away and we restart from `i+1`. The work done for the valid prefix is wasted.

**State out loud:** "Brute force: O(n²) — for each start, extend until I hit a duplicate. The sliding-window optimal does it in O(n)."

---

## 2. Optimal — Sliding Window (O(n))

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        window = set()
        left = 0
        best = 0

        for right in range(len(s)):
            while s[right] in window:
                window.remove(s[left])
                left += 1
            window.add(s[right])
            best = max(best, right - left + 1)

        return best
```

### How it works

- **R walks forward** through every position once.
- **L only moves when the window has a duplicate** — it shrinks from the left until the duplicate is gone.
- **Each character visited at most TWICE** (once by R, at most once by L). That's the O(n) magic.

### Sliding window vs converging two-pointer

| | Sliding window (LC 3) | Converging two-pointer (LC 167, LC 15) |
|---|---|---|
| Start positions | both at 0 | L at 0, R at end |
| Direction | both move FORWARD | move TOWARD each other |
| Loop condition | `for right in range(len(s))` | `while left < right` |
| When L moves | when invariant breaks (duplicate) | every iteration based on sum comparison |
| When R moves | every iteration | sometimes |

Different pattern. Don't reach for `left, right = 0, n-1` on sliding-window problems.

### Complexity

- **Time:** O(n) — each character is visited at most twice (R adds it once, L removes it at most once).
- **Space:** O(min(n, |alphabet|)) — the set holds at most |alphabet| distinct characters (~128 for ASCII).

---

## 3. Brute Force vs Sliding Window

| Aspect              | Brute Force (O(n²))         | Sliding Window (O(n))         | Winner       |
|---------------------|------------------------------|--------------------------------|--------------|
| Time                | O(n²)                        | O(n)                           | Sliding Win  |
| Space               | O(min(n, alphabet))          | O(min(n, alphabet))            | Tie          |
| Reuses prior work?  | No — restarts from each i    | Yes — drops the duplicate only | Sliding Win  |
| Lines of code       | ~10                          | ~10                            | Tie          |
| n=50,000 ops        | ~2.5 billion                 | ~100,000                       | Sliding Win  |

---

## 4. Test Cases

| s            | Expected | Notes |
|--------------|----------|-------|
| `"abcabcbb"` | 3        | Canonical example — "abc" |
| `"bbbbb"`    | 1        | All same — best is 1 |
| `"pwwkew"`   | 3        | "wke" — not "pwke" (non-contiguous) |
| `""`         | 0        | Empty input |
| `"a"`        | 1        | Single char |
| `"au"`       | 2        | Two distinct |
| `"dvdf"`     | 3        | "vdf" — shows L moves past 'd' |
| `" "`        | 1        | Single space — spaces count |

---

## 5. Interview Out-Loud Explanation

> "Brute force is O(n²) — for each starting position, extend until I hit a duplicate. But that wastes work — when I hit the duplicate, I throw away the valid prefix and restart.
>
> The optimal is **sliding window**, O(n). I maintain a window of characters from index `left` to `right`. R walks forward through every position, adding the character at R to the window. If adding it would create a duplicate, I shrink the window from the LEFT — remove `s[left]`, advance `left` — until the duplicate is gone. Then add the new character.
>
> Each character is visited at most twice — once by R, once by L. That's how I get linear time.
>
> Space is O(min(n, alphabet)) for the set tracking what's in the window."

---

## 6. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Reaching for converging two-pointer | `left, right = 0, n-1` — wrong pattern, pointers should both move forward | Both start at 0; R walks via `for right in range(...)` |
| Forgetting to update `best` | Loop finishes but `best` never updated when window stays valid | `best = max(best, right - left + 1)` every iteration |
| Adding before checking duplicate | Adds the duplicate, then has to deal with it | Check `while s[right] in window` BEFORE adding |
| Using `if` instead of `while` for shrink | Window may still contain the duplicate after one shrink | `while s[right] in window` — keep shrinking until gone |
| Off-by-one on window size | Window size is `right - left + 1`, not `right - left` | Always +1 (both ends inclusive) |

---

## Likely Follow-ups

The interview is one question that grows in parts — expect the problem to mutate after your first solution works.

- **"Now return the substring itself, not just the length."** → Track the start index of the best window when you update `best`. Return `s[start:start+best]`.
- **"What if up to k repeats of a character are allowed?"** → Same window skeleton, different shrink condition. That is literally LC 424 Longest Repeating Character Replacement, the next script in this chain.
- **"What if the input is a stream of characters, not a string?"** → The window already reads left to right. Keep the set and a deque of window chars; no random access needed.
- **"Can you avoid re-scanning when you hit a duplicate?"** → Store each char's last-seen index in a dict and jump `left` straight past it, instead of shrinking one step at a time.

---

**Chain position:** sliding-window intro for the prep plan. Appears in: LC 424 Longest Repeating Character Replacement, LC 76 Minimum Window Substring, LC 567 Permutation in String, LC 438 Find All Anagrams in String.

Master this pattern and 5+ other Phase B problems become much easier.
