# LC 217 — Contains Duplicate · Practice Script

---

## Problem Statement (Simple Version)

> Given an integer array `nums`, return `true` if any value appears **at least twice**,  
> otherwise return `false`.

**Examples:**
- `[1,2,3,1]` → `true` (1 appears twice)
- `[1,2,3,4]` → `false`
- `[1,1,1,3,3,4,3,2,4,2]` → `true`

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Can the array be empty or have one element?"** — Yes. Both return `false` — no pair possible.
- **"Do you want WHICH value repeats, or just true/false?"** — Just true/false. That's why a set is enough; a dict would be needed for indices.
- **"Are values bounded to a small range?"** — If yes, a fixed-size boolean array beats a set. Here they're unbounded, so set.
- **"Can I modify the input?"** — If yes, sorting in place and checking neighbors gives O(1) extra space at O(n log n) time.

---

## Why This Problem Feels Harder Than Two Sum

Two Sum was about **finding a pair** using a hashmap.  
Contains Duplicate is about **detecting if something already exists**.

The jump comes from:
- You need to think about **sets** instead of just dictionaries
- The logic is slightly more abstract
- You have to decide: "Do I need to store the index, or just the existence?"

This is exactly the kind of "slightly harder" medium problem you should be comfortable with in coding interviews.

---

## Solution 1: Brute Force (Two Nested Loops)

```python
from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j]:
                    return True
        return False
```

**Time Complexity:** O(n²)  
**Why it's bad:** Same problem as brute force Two Sum — it becomes very slow for large arrays.

---

## Solution 2: Optimal (HashSet) — Recommended

```python
from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()                    # we only care about existence, not index

        for num in nums:
            if num in seen:
                return True             # we found a duplicate!
            seen.add(num)
        
        return False                    # no duplicates found
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

---

## ALTERNATIVE — One-liner (`len(set(nums)) != len(nums)`)

```python
from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))
```

This version shows you understand Python well. Many strong candidates use this.

---

## Key Points

1. **Why use a set instead of a dict?**  
   We only need to know *if* a number was seen before — we don't need the index. A set is cleaner and uses less memory.

2. **Why check BEFORE adding?**  
   Same logic as Two Sum. We want to detect if we have seen this number **previously**.

3. **Edge cases to mention:**
   - Empty array → return `false`
   - Array with one element → return `false`
   - All elements the same → return `true`
   - All elements unique → return `false`

---

## Test Cases (You Should Be Able to Explain These)

| Input                              | Expected | Why |
|------------------------------------|----------|-----|
| `[1,2,3,1]`                        | `true`   | 1 appears twice |
| `[1,2,3,4]`                        | `false`  | All unique |
| `[]`                               | `false`  | Empty array |
| `[1]`                              | `false`  | Only one element |
| `[1,1,1,1]`                        | `true`   | All same |
| `[1,2,3,4,5,6,7,8,9,1]`            | `true`   | 1 appears at the end |

---

## How to Practice This Problem (Recommended Flow)

1. **Read the problem** slowly
2. **Write brute force** first (even if you know it's bad)
3. **Explain the disadvantage** out loud (`O(n²)`)
4. **Write the optimal set version**
5. **Explain why set is better** than dict here
6. **Write 5–6 test cases yourself**
7. **Close the file and retape** the optimal solution from memory
8. **Record yourself** explaining the solution once

---

## Interview Out-Loud

> "For this problem I can use a hashset. I'll go through the array once.  
> For each number, I check if I've already seen it before.  
> If yes, I return true immediately.  
> If not, I add it to the set.  
> At the end, if I never found a duplicate, I return false.  
> This gives us O(n) time and O(n) space.  
> I could also use a dictionary, but a set is cleaner because I only need to track existence, not the index."

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Using `{}` for empty set | That's an empty dict — `1 in {}` works but `.add` doesn't | Use `set()` for empty set |
| Adding BEFORE checking | First sighting of every element triggers `True` falsely (only if you re-iterate) | Check `if num in seen:` BEFORE `seen.add(num)` |
| Iterating with a list and `in` check | `x in list` is O(n) → total O(n²) | Use a set: `x in set` is O(1) |
| Returning at end without checking | The `return False` after the loop is critical | Add `return False` after the loop ends |
| Using a dict when a set is enough | Wastes space (storing dummy values) | Use `set` when you only need existence, not index |

---

## Likely Follow-ups

The interview is one question that grows in parts — expect this one to mutate once your set version works.

- **"Now return WHICH values are duplicated."** → Swap the set for a dict of counts, or keep a second set of repeats. Return its contents at the end.
- **"True only if the duplicate is within k positions."** → That's Contains Duplicate II. Keep a sliding-window set of the last k values: add on entry, remove on exit.
- **"The input is a huge stream that doesn't fit in memory."** → Exact answer needs external sort (sort chunks, check neighbors). For an approximate answer, mention a Bloom filter.
- **"No extra space allowed."** → Sort in place, then one pass comparing each element to its neighbor. O(n log n) time, O(1) space.

---

## Chain position

Contains Duplicate is the **set existence pattern**. The bouncer-with-a-guest-list idea extends to:
- **Longest Consecutive Sequence** — Hash Set with anchor check
- **Word Search** (Phase C) — set of visited cells
- **Happy Number** — set of seen values for cycle detection
- **Linked List Cycle** — same concept (though slow/fast pointers is the canonical answer there)

The "have I seen this before?" question is one of the most common signals in coding interviews. Master the O(1) set lookup as your default reflex.