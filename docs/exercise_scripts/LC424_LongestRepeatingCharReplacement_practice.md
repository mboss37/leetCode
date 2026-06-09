# LC 424 — Longest Repeating Character Replacement · Practice Script

---

## Problem

> You're given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English letter — at most `k` times. Return the **length of the longest substring** containing the same letter you can get after performing these changes.

**Constraints:**
- `1 <= s.length <= 10⁵`
- `s` consists of uppercase English letters only.
- `0 <= k <= s.length`

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Is the string only uppercase A-Z?"** — Yes. So the count map caps at 26 entries — effectively O(1) space.
- **"Can k be 0?"** — Yes. Then it's just the longest run of one repeated char — the same code handles it.
- **"Do I replace with any letter, or only letters already in the string?"** — Any letter. And we never actually replace — we only count how many we WOULD need.
- **"Return the length or the substring itself?"** — Length only. The substring would mean recording the window start whenever best updates.
- **"Can k be larger than the string length?"** — Yes. Then the whole string is the answer; the window just never shrinks.

---

## NOT RECOMMENDED — Check Every Substring (O(n³))

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        n = len(s)
        best = 0
        for i in range(n):
            for j in range(i, n):
                counts = {}
                for c in s[i:j+1]:
                    counts[c] = counts.get(c, 0) + 1
                max_count = max(counts.values())
                length = j - i + 1
                if length - max_count <= k:
                    best = max(best, length)
        return best
```

- **Time:** O(n³) — n² substrings × O(n) char count.
- For n = 10⁵: 10¹⁵ ops → TLE.

State verbally:
> *"Brute force is check every substring: count its most frequent char and see if `length - max_count ≤ k`. O(n³). Better: a sliding window that grows while `length - max_count ≤ k` and shrinks otherwise — O(n)."*

---

## RECOMMENDED — Sliding Window with Max-Count (O(n))

```python
from collections import defaultdict

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        counts = defaultdict(int)
        left = 0
        best = 0
        max_count = 0

        for right in range(len(s)):
            counts[s[right]] += 1
            max_count = max(max_count, counts[s[right]])

            while (right - left + 1) - max_count > k:
                counts[s[left]] -= 1
                left += 1

            best = max(best, right - left + 1)

        return best
```

### The key invariant

A window is **VALID** iff:
```
window_size − max_count ≤ k
```

That is: the number of "non-majority" characters in the window (which we'd need to REPLACE) is at most k.

`max_count` = the count of the most frequent character in the window.

### Why `max_count` doesn't need to be decremented on shrink

When you shrink from the left and decrement `counts[s[left]]`, the true max could decrease. But we DON'T decrement `max_count`. Why is that safe?

- `best` is updated only when the window is VALID.
- A valid window requires `window_size ≤ max_count + k`.
- If `max_count` is stale (too big), the algorithm thinks the window is valid when maybe it's not.
- BUT: `best` only ever GROWS — it tracks the MAX size seen. The stale `max_count` doesn't shrink `best`; it just keeps the window-size check generous.
- The OPTIMAL answer always involves a window where `max_count` was correct at the time — and at that moment, `best` was updated correctly.

So a stale (too-large) `max_count` is harmless. It saves us the cost of recomputing the true max on every shrink (which would be O(26) per shrink → O(n) total — still fine but ugly).

### Trace on `s = "AABABBA"`, `k = 1`

| R | s[R] | counts | max_count | window | (size − max) ≤ k? | best |
|---|---|---|---|---|---|---|
| 0 | A | {A:1} | 1 | "A" | 1-1=0 ≤ 1 ✓ | 1 |
| 1 | A | {A:2} | 2 | "AA" | 2-2=0 ≤ 1 ✓ | 2 |
| 2 | B | {A:2,B:1} | 2 | "AAB" | 3-2=1 ≤ 1 ✓ | 3 |
| 3 | A | {A:3,B:1} | 3 | "AABA" | 4-3=1 ≤ 1 ✓ | 4 |
| 4 | B | {A:3,B:2} → {A:2,B:2} | 3 | "AABAB" → "ABAB" | 5-3=2 > 1 → shrink. drop A, left=1. 4-3=1 ≤ 1 ✓ | 4 |
| 5 | B | {A:2,B:3} → {A:1,B:3} | 3 | "ABABB" → "BABB" | 5-3=2 > 1 → shrink. drop A, left=2. 4-3=1 ≤ 1 ✓ | 4 |
| 6 | A | {A:2,B:3} → {A:2,B:2} | 3 | "BABBA" → "ABBA" | 5-3=2 > 1 → shrink. drop B, left=3. 4-3=1 ≤ 1 ✓ | 4 |

Returns **4** ✓

### Complexity

- **Time:** O(n) — each char visited at most twice (once by right, at most once by left)
- **Space:** O(k) — counts dict capped at 26 letters → effectively O(1)

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Decrementing `max_count` on shrink | O(26) recomputation per shrink — slower | Leave stale; best only grows so it's safe |
| Using `if` instead of `while` for shrink | Window might still be invalid after one shrink | `while window_size - max_count > k` |
| Wrong invariant: `max_count + k >= window_size` written backwards | Treat invalid windows as valid | Use `(right - left + 1) - max_count > k` for the SHRINK trigger |
| Forgetting to update `max_count` on right expansion | Window expands but max not tracked | `max_count = max(max_count, counts[s[right]])` every iteration |

---

## Interview Out-Loud

> "Sliding window. Track the count of each char in the window plus the max count (most frequent char). Window is VALID iff `window_size - max_count ≤ k` — that's how many non-majority chars we'd need to replace.
>
> R walks every char, incrementing its count and updating max_count. When the invariant breaks (size - max_count > k), shrink from L until valid. Update best every iteration.
>
> Trick: don't bother decrementing max_count on shrink. It can stay stale; best only grows, so a too-large max_count just keeps the window-size check generous — never causes incorrect updates.
>
> O(n) time, O(1) space (26 chars max)."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect one of these next:

- **"Return the substring, not just the length."** → Save `left` whenever `best` updates; return `s[best_left : best_left + best]` at the end.
- **"Longest substring with at most k DISTINCT characters?"** → Same window shape, new invariant: shrink while `len(counts) > k` (LC 340). Compare with LC 3 — there's a practice script for it in this repo.
- **"Minimum replacements to make the WHOLE string one letter?"** → No window needed: `len(s) - max frequency`.
- **"What if the alphabet is huge (unicode)?"** → Logic unchanged; the counts dict just isn't capped at 26 anymore, so space grows with distinct chars.

---

**Chain position:** Sliding window with invariant check. Generalizes to: Longest Substring with At Most K Distinct, Permutation in String, Find All Anagrams.
