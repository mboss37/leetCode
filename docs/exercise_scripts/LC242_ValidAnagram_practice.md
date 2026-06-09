# LC 242 — Valid Anagram · Practice Script

---

## Problem Statement

Given two strings `s` and `t`, return `true` if `t` is an **anagram** of `s`, and `false` otherwise.

An anagram is a word formed by rearranging the letters of another word, using **all** the original letters **exactly once**.

**Examples:**
- `s = "anagram"`, `t = "nagaram"` → `true`
- `s = "rat"`, `t = "car"` → `false`
- `s = "aacc"`, `t = "ccac"` → `true`

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Lowercase English letters only, or full Unicode?"** — Lowercase per spec. Unicode means the "26 keys" space claim changes, but Counter handles it unchanged.
- **"Is it case sensitive? Do spaces count?"** — Per spec yes and there are none. If not, normalize with `.lower()` and strip spaces first.
- **"Can the strings have different lengths?"** — Yes, and that's an instant `False` — check lengths first, it's the cheapest exit.
- **"Are both strings empty a valid anagram?"** — Yes, `"" / ""` → `True`. Both loops just never run.
- **"Can I use library helpers like Counter?"** — Usually yes. If blocked, write the manual frequency map (Solution 3).

---

## Solution 1: Sorting (Brute Force / Simple)

```python
from typing import List

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # If lengths are different → cannot be anagrams
        if len(s) != len(t):
            return False
        
        # Sort both strings alphabetically and compare
        return sorted(s) == sorted(t)
```

**Time Complexity:** O(n log n)  
**Space Complexity:** O(1) (sorting creates new strings, but acceptable)

**Why this is NOT recommended as the main solution:**

- It works and is very easy to write.
- However, it is **O(n log n)** because sorting requires multiple passes and comparisons.
- It does **not** show strong understanding of data structures.
- In coding interviews, they want to see if you can find the **better** solution when it exists.

---

## Solution 2: `Counter(s) == Counter(t)` (Recommended — Lead with this)

```python
from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
```

**Time Complexity:** O(n) — `Counter` walks each string once
**Space Complexity:** O(1) — at most 26 keys (lowercase English letters only)

**Why this is the lead solution:**
- One line. Reads like the problem statement.
- Same O(n) complexity as a manual hashmap — no signal lost.
- `Counter` is canonical stdlib Python for "frequency map" — using it shows you know your tools.
- Equality on `Counter` objects compares all (key, count) pairs directly.

If the interviewer asks *"do it without `Counter`"* — see Solution 3 below.

---

## Solution 3: Manual Frequency Map (follow-up if asked)

Same algorithm, spelled out by hand. Useful for understanding what `Counter` does under the hood, and to write when the interviewer explicitly blocks the stdlib.

```python
from typing import List

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        seen = {}                    # character -> frequency
        
        # Count characters in first string
        for char in s:
            seen[char] = seen.get(char, 0) + 1
        
        # Subtract characters from second string
        for char in t:
            if char not in seen:
                return False
            seen[char] -= 1
            if seen[char] == 0:
                del seen[char]
        
        return len(seen) == 0
```

**Time Complexity:** O(n) — single pass through each string  
**Space Complexity:** O(1) — at most 26 keys (lowercase English letters only)

### Trace on `s = "anagram"`, `t = "nagaram"`

After the first loop (count chars in `s`):

| step | char | seen                          |
|------|------|-------------------------------|
| init | —    | `{}`                          |
| 1    | a    | `{a: 1}`                      |
| 2    | n    | `{a: 1, n: 1}`                |
| 3    | a    | `{a: 2, n: 1}`                |
| 4    | g    | `{a: 2, n: 1, g: 1}`          |
| 5    | r    | `{a: 2, n: 1, g: 1, r: 1}`    |
| 6    | a    | `{a: 3, n: 1, g: 1, r: 1}`    |
| 7    | m    | `{a: 3, n: 1, g: 1, r: 1, m: 1}` |

Then subtract for each char in `t` (delete on hit zero):

| char | seen (after)                     |
|------|----------------------------------|
| n    | `{a: 3, g: 1, r: 1, m: 1}`       |
| a    | `{a: 2, g: 1, r: 1, m: 1}`       |
| g    | `{a: 2, r: 1, m: 1}`             |
| a    | `{a: 1, r: 1, m: 1}`             |
| r    | `{a: 1, m: 1}`                   |
| a    | `{m: 1}`                         |
| m    | `{}`                             |

Empty dict at the end → `True`. **The delete-on-zero matters** — without it, `len(seen) == 0` never holds and you'd need a different end check.

**Why this is RECOMMENDED:**

- Much faster for longer strings (O(n) vs O(n log n))
- Shows you understand **frequency counting** — a core pattern used in many medium problems
- Uses constant space (bounded by 26 letters)
- Clean, professional, and easy to explain

---

## Comparison Table

| Aspect                  | Sorting Version          | Hashmap Version              | Winner          |
|-------------------------|--------------------------|------------------------------|-----------------|
| Time Complexity         | O(n log n)               | **O(n)**                     | Hashmap         |
| Space Complexity        | O(1)                     | O(1)                         | Tie             |
| Code simplicity         | Very simple              | Slightly more code           | Sorting         |
| What it demonstrates    | Basic Python knowledge   | **Frequency counting + hashmap** | Hashmap     |
| Interview signal        | Acceptable               | **Strong**                   | Hashmap         |

---

## Key Points

1. **Always check length first** — different lengths = not anagrams.
2. **Two common approaches:**
   - Sorting (simple, O(n log n))
   - Hashmap / Counter (optimal, O(n), shows frequency counting)
3. **This pattern appears in many medium problems:**
   - Group Anagrams
   - Top K Frequent Elements
   - Longest Repeating Character Replacement

---

## Test Cases

| s              | t              | Expected |
|----------------|----------------|----------|
| "anagram"      | "nagaram"      | true     |
| "rat"          | "car"          | false    |
| "aacc"         | "ccac"         | true     |
| "ab"           | "a"            | false    |
| ""             | ""             | true     |
| "abc"          | "def"          | false    |

---

## Interview Out-Loud

> "First I check if the lengths are different — if they are, it's impossible to be an anagram.  
> The simple solution is to sort both strings and compare them, but that's O(n log n).  
> Instead, I use a hashmap to count the frequency of every character in the first string in one pass.  
> Then I go through the second string and subtract the counts.  
> If I ever see a character that doesn't exist or goes negative, I return false.  
> At the end, if the hashmap is empty, both strings have exactly the same character counts, so I return true.  
> This runs in O(n) time and uses constant space (at most 26 keys)."

---

## Recommended Practice Flow (Daily)

1. Read the problem statement out loud
2. Write the **sorting version** from memory (2 min)
3. Write the **hashmap version** from memory (5 min)
4. Explain the trade-off between sorting vs hashmap out loud
5. Run the test cases mentally or in code
6. Retape the hashmap version once without looking

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Skipping the length check | Wastes work building hashmaps that can never match | `if len(s) != len(t): return False` FIRST |
| Tracking indices instead of counts | Two values with the same character get collapsed (collision) | Track COUNTS, not indices |
| `dict.get(c, 1) + 1` for first sight | Off-by-one: first sighting becomes 2 instead of 1 | Use `dict.get(c, 0) + 1` |
| Using `sorted(s) == sorted(t)` when interviewer asks for optimal | O(n log n) when O(n) is possible | State sort verbally, use Counter for code |
| Forgetting Unicode | `.lower()` matters for case-sensitive variants | Read the spec — most are case-sensitive |

---

## Likely Follow-ups

The interview is one question that grows in parts — expect the anagram check to become a building block.

- **"Now group a whole list of words into anagram groups."** → That's Group Anagrams (LC 49). Hash map keyed by sorted word (or by the count tuple), values are lists.
- **"What if the input is Unicode?"** → The fixed-26 assumption dies; a dict/Counter still works. Mention that "constant space" becomes O(k) for k distinct characters.
- **"Find every anagram of `s` inside a long string."** → Sliding window of length `len(s)` over the long string, compare two frequency maps as the window moves.
- **"Do it without Counter."** → The manual frequency map: count chars of `s`, subtract chars of `t`, fail on missing or negative, succeed if the map empties.

---

## Chain position

Valid Anagram is the **frequency-counting pattern**. The same Counter-based approach extends to:
- **Group Anagrams** — `defaultdict(list)` keyed by sorted letters (or by Counter-as-tuple)
- **Top K Frequent Elements** — `Counter.most_common(k)`
- **Find All Anagrams in a String** — sliding window with two Counters
- **Valid Anagram Permutation** (in Phase B problems)

The `Counter(s) == Counter(t)` idiom is Pythonic shorthand for an entire category of equality-by-frequency problems.