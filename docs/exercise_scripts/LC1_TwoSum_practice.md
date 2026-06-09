# LC 1 — Two Sum · Practice Script

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Is the array sorted?"** — No. If it were, two pointers with O(1) space would beat the hash map (that's LC 167).
- **"Can I use the same element twice?"** — No. Same index twice is banned, but two equal values at different indices are fine (`[3,3]`, target 6).
- **"Is there always exactly one solution?"** — Yes per spec. If none were possible, agree on a return value like `[]`.
- **"Do you want indices or values?"** — Indices. That's why the hash map stores value → index.
- **"Can numbers be negative? Zero?"** — Yes, both. Neither breaks the hash map.

---

## 1. Brute Force Solution (O(n²))

```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):                    # outer loop
            for j in range(i + 1, len(nums)):         # inner loop starts after i
                if nums[i] + nums[j] == target:
                    return [i, j]
        
        return []                                     # no solution found
```

### Why Brute Force is NOT Optimal

- **Time Complexity:** O(n²)
- **Formula:** Total comparisons = `n(n-1)/2`
  - Example with n=5: `5 × 4 / 2 = 10` comparisons
  - Example with n=1000: ~500,000 comparisons
- For large arrays this becomes very slow and can cause timeouts.
- We check **every possible pair** even though we only need one.

**Interview line you should say:**
> "The brute force solution uses two nested loops and performs n(n-1)/2 comparisons, which is O(n²). This works for small arrays but becomes inefficient for larger inputs — that's why we need a better approach."

---

## 2. Optimal Hashmap Solution (O(n))

```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}                              # hashmap: value -> index

        for i, num in enumerate(nums):
            complement = target - num          # what we still need to reach the target
            if complement in seen:
                return [seen[complement], i]   # found the pair!
            seen[num] = i                      # store current value + its index

        return []                              # no solution found
```

---

## 3. Comparison: Brute Force vs Hashmap

| Aspect              | Brute Force                  | Hashmap (Optimal)             | Winner     |
|---------------------|------------------------------|-------------------------------|------------|
| Time Complexity     | O(n²)                        | O(n)                          | Hashmap    |
| Space Complexity    | O(1)                         | O(n)                          | Brute Force|
| Number of passes    | 2 nested loops               | Single pass                   | Hashmap    |
| Readability         | Simple                       | Slightly more complex         | —          |
| Real-world use      | Only for very small arrays   | Production standard           | Hashmap    |

---

## 4. How to Practice This Script (Daily Flow)

### Step 1: Read this explanation out loud (2–3 min)

> "The brute force approach with two nested loops is O(n²) because we perform n(n-1)/2 comparisons.  
> Instead, I use a hashmap to achieve O(n) time in a single pass.  
> As I iterate through the array, I calculate the complement for each number.  
> If the complement already exists in the hashmap, I return the pair immediately.  
> Otherwise, I store the current number and its index.  
> I check before storing to avoid pairing a number with itself."

### Step 2: Key Points to Memorize

- **Brute Force:** O(n²) — n(n-1)/2 comparisons
- **Hashmap:** O(n) time, O(n) space
- **Why check BEFORE storing?**  
  We only want to pair with a **previously seen** number. Storing first could cause us to pair a number with itself (e.g. `[3,3]` target 6).
- **enumerate()** gives us both index and value in one loop.

### Step 3: Test Cases (Run These Manually)

| nums                  | target | Expected Output | Notes |
|-----------------------|--------|------------------|-------|
| [2, 7, 11, 15]        | 9      | [0, 1]           | Basic case |
| [3, 2, 4]             | 6      | [1, 2]           | Not first pair |
| [3, 3]                | 6      | [0, 1]           | Duplicate values (critical test) |
| [1, 5, 3]             | 8      | [0, 2]           | — |
| []                    | 5      | []               | Empty array |
| [1]                   | 5      | []               | Single element |
| [-1, -2, -3]          | -5     | [1, 2]           | Negative numbers |

### Step 4: Full Testing Code (Copy-Paste & Run Locally)

```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []


# ====================== TEST CASES ======================
solution = Solution()

print(solution.twoSum([2, 7, 11, 15], 9))     # Expected: [0, 1]
print(solution.twoSum([3, 3], 6))             # Expected: [0, 1]
print(solution.twoSum([3, 2, 4], 6))          # Expected: [1, 2]
print(solution.twoSum([], 5))                 # Expected: []
print(solution.twoSum([-1, -2, -3], -5))      # Expected: [1, 2]
```

---

## Interview Out-Loud

> "The brute force approach uses two nested loops and performs n(n-1)/2 comparisons, which gives O(n²) time complexity. This works for small inputs but becomes too slow for larger arrays.  
> Instead, I use a hashmap to solve this in O(n) time with a single pass.  
> As I iterate through the array, I calculate the complement for each number.  
> If the complement already exists in the hashmap, I return the two indices immediately.  
> Otherwise, I store the current number and its index.  
> I always check before storing to avoid pairing a number with itself."

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Check AFTER adding (`seen[num] = i` before `if complement in seen`) | Could match a number with itself (e.g., `[3, 3]` target 6 → would return `[0, 0]`) | Always check BEFORE adding |
| `seen[complement]` lookup if `complement not in seen` | KeyError | Check `if complement in seen:` first |
| Returning the values instead of indices | Spec wants indices | Return `[seen[complement], i]`, not the values |
| Using `dict.get(complement)` and comparing to None | Confusing — `None` is falsy but so is `0` | Use `if complement in seen:` — explicit |

---

## Likely Follow-ups

The interview is one question that grows in parts — expect Two Sum to mutate after you finish it.

- **"What if the array is sorted?"** → Two pointers from both ends, O(1) space. That is exactly LC 167 Two Sum II — the next script in this chain.
- **"Now find three numbers that sum to the target."** → Sort, fix an anchor, run two pointers on the rest. That is LC 15 3Sum.
- **"Return ALL pairs, not just the first."** → Don't return early; collect matches and agree with the interviewer how duplicate pairs are handled.
- **"What if the numbers arrive as a stream?"** → Same hash map, built as values arrive: check the complement, then store. One pass, no second look needed.

---

## Chain position

Two Sum is the **foundation hash-map pattern**. The "magic notebook of complements" idea extends to:
- **Two Sum Sorted** — same problem, sorted input → two pointers instead of hash map
- **3Sum / 4Sum** — sort + outer loop + Two Sum
- **Group Anagrams** — hash map of lists, key by sorted letters
- **Longest Consecutive Sequence** — hash map for O(1) membership + anchor check

Master this one cold — it's the gateway to half of Phase A and B.