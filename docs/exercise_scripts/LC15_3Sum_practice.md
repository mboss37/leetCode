# LC 15 — Three Sum · Practice Script

---

## Problem (LeetCode 15)

> Given an integer array `nums`, return all the **triplets** `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.
> The solution set must **not contain duplicate triplets**.

**Constraints:**
- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

**Key trap:** "no duplicate triplets" applies to **value-level** dedup. The positions can be different; the sorted triplet of values must be unique in the output set.

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Do you want the values or the indices?"** — Values. That's what makes sorting legal — sorting destroys original indices.
- **"Are duplicate triplets allowed in the output?"** — No. Dedup is by VALUES, not positions — `[-1, -1, 2]` may only appear once.
- **"May I modify (sort) the input array?"** — Usually yes. If not, sort a copy — costs O(n) space, same algorithm.
- **"Does output order matter?"** — No. So no extra sorting of the result is needed.
- **"What if no triplet sums to zero, or the array is tiny?"** — Return an empty list. Constraints say n ≥ 3, but `[]` covers smaller defensively.

---

## 1. Brute Force Solution (O(n³))

```python
from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        final_list = set()                              # auto-dedupes tuples

        for i in range(n):                              # anchor 1
            for j in range(i + 1, n):                   # anchor 2 (j > i)
                for k in range(j + 1, n):               # anchor 3 (k > j)
                    if nums[i] + nums[j] + nums[k] == 0:
                        # sort normalizes the order; tuple makes it hashable
                        triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                        final_list.add(triplet)

        return [list(t) for t in final_list]
```

### Why Brute Force is NOT Optimal

- **Time Complexity:** O(n³)
- **Formula:** ~`n³/6` triplet checks (`C(n, 3)`)
  - n=100: ~166,000 checks
  - n=500: ~21,000,000 checks
  - n=3000: ~4.5 BILLION checks — way too slow
- We check **every triple of positions** even though most won't sum to zero.
- Value-level dedup is handled by sorting each triplet and storing as a **tuple** in a **set**.
- Lists can't go in a set (lists are mutable → unhashable). Tuples are immutable → hashable.

**Interview line you should say:**
> "Brute force is three nested loops giving O(n³). For LC 15 constraints (n ≤ 3000), that's ~4.5 billion operations — too slow. I'll use sort + two pointers for O(n²) instead."

---

## 2. Optimal Two-Pointer Solution (O(n²))

```python
from typing import List

class Solution:
    def threeSum(self, numbers: List[int]) -> List[List[int]]:
        sorted_nums = sorted(numbers)                   # sort unlocks two-pointer + dedup
        n = len(sorted_nums)
        result = []

        for i in range(n - 2):                          # anchor — stop at n-3 (need 2 more)
            # SKIP 1: duplicate anchors
            if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
                continue

            left, right = i + 1, n - 1                  # fresh pointers per anchor

            while left < right:
                current_sum = sorted_nums[i] + sorted_nums[left] + sorted_nums[right]

                if current_sum == 0:
                    result.append([sorted_nums[i], sorted_nums[left], sorted_nums[right]])

                    # SKIP 2: duplicate L values
                    while left < right and sorted_nums[left] == sorted_nums[left + 1]:
                        left += 1
                    # SKIP 3: duplicate R values
                    while left < right and sorted_nums[right] == sorted_nums[right - 1]:
                        right -= 1

                    left += 1                            # advance into fresh territory
                    right -= 1

                elif current_sum < 0:
                    left += 1                            # sum too small → bigger L
                else:
                    right -= 1                           # sum too big → smaller R

        return result
```

### Why This Works (key invariants)

1. **Sorting groups duplicate values into contiguous blocks.** That's what makes the three skip checks correct — each one only looks at the IMMEDIATE neighbor (`i-1`, `L+1`, `R-1`), and because duplicates sit next to each other, that's enough.

2. **Skip 1 — anchor:** if `sorted_nums[i] == sorted_nums[i-1]`, the previous anchor (same value) explored a superset of what this anchor would find. Anything we'd find here is a duplicate of something already recorded.
   > **The line to remember:** *"Any triplet the second anchor finds, the first already found."*

3. **Skip 2 — L:** after a match, walk L past duplicate-value neighbors so the next inner iteration starts on a fresh value.

4. **Skip 3 — R:** mirror of skip 2 on the R side.

5. **No set needed.** The three skips guarantee that each unique value-triplet has exactly ONE path through `(i, L, R)`. Dedup happens at the **traversal** level, not the **storage** level. Output order is deterministic.

---

## 3. Comparison: Brute Force vs Two-Pointer

| Aspect              | Brute Force (O(n³))            | Two-Pointer (O(n²))             | Winner       |
|---------------------|--------------------------------|----------------------------------|--------------|
| Time Complexity     | O(n³)                          | O(n²)                            | Two-Pointer  |
| Space Complexity    | O(k) for the set               | O(1) auxiliary                   | Two-Pointer  |
| Dedup mechanism     | Set of sorted tuples           | Skip-duplicate logic             | Two-Pointer  |
| Readability         | Simple — 3 nested loops        | Moderate — 3 skip checks         | Brute Force  |
| Output order        | Non-deterministic (set)        | Deterministic (input order)      | Two-Pointer  |
| Real-world use      | Only tiny inputs (n < 50)      | Production standard              | Two-Pointer  |
| Generalizes to 4Sum?| Yes, but slower (O(n⁴))        | Yes, with another nested loop    | Two-Pointer  |

---

## 4. How to Practice This Script (Daily Flow)

### Step 1: Read this explanation out loud (2–3 min)

> "Brute force is three nested loops, O(n³), with a set of sorted tuples for value-level dedup. It works but is too slow once n gets past a few hundred.
> The optimal approach sorts the array first. Sorting is O(n log n) but unlocks two benefits — it lets me reason about the two-pointer sum (moving L right increases the sum, moving R left decreases it), AND it groups duplicates next to each other so I can skip them by checking adjacent positions.
> The outer loop fixes one element as the anchor. For each anchor I run a two-pointer scan over the remaining slice, looking for L + R = -anchor. That's essentially LC 167 with a fixed target.
> Three skip checks prevent duplicate triplets: skip duplicate anchors at the top of the outer loop, and after each match walk L and R past their duplicate neighbors before advancing.
> Total time O(n²), aux space O(1). No set required."

### Step 2: Key Points to Memorize

- **Brute Force:** O(n³) time, O(k) space (set of tuples). State this, don't write it.
- **Optimal:** O(n²) time, O(1) auxiliary space.
- **Why sort?** TWO reasons:
  1. Enables two-pointer reasoning.
  2. Groups duplicates contiguously for O(1) skip checks.
- **`i > 0` guard:** Python's negative indexing means `sorted_nums[-1]` silently returns the LAST element. Without the guard, this would produce a meaningless comparison.
- **On match, advance BOTH pointers** — the match branch is isolated by the `elif` chain. You must move L and R yourself inside that branch.
- **Reset pointers INSIDE the outer loop.** Each anchor needs fresh L = i+1, R = n-1.

### Step 3: Test Cases (Run These Manually)

| nums                          | Expected Output                            | Notes                          |
|-------------------------------|--------------------------------------------|--------------------------------|
| `[-1, 0, 1, 2, -1, -4]`       | `[[-1, -1, 2], [-1, 0, 1]]`                | Canonical example              |
| `[]`                          | `[]`                                       | Empty                          |
| `[0]`                         | `[]`                                       | Too small                      |
| `[0, 0, 0]`                   | `[[0, 0, 0]]`                              | All zeros (single triplet)     |
| `[0, 0, 0, 0]`                | `[[0, 0, 0]]`                              | Dedup test — only ONE triplet  |
| `[1, 2, 3]`                   | `[]`                                       | No triplet sums to 0           |
| `[-2, 0, 1, 1, 2]`            | `[[-2, 0, 2], [-2, 1, 1]]`                 | Duplicates in input            |
| `[3, 0, -2, -1, 1, 2]`        | `[[-2, -1, 3], [-2, 0, 2], [-1, 0, 1]]`    | Mixed positive / negative      |
| `[-2, -1, -1, 0, 0, 1, 1, 2]` | `[[-2, 0, 2], [-2, 1, 1], [-1, -1, 2], [-1, 0, 1]]` | Heavy duplicates — dedup test |

### Step 4: Full Testing Code (Copy-Paste & Run Locally)

```python
from typing import List

class Solution:
    def threeSum(self, numbers: List[int]) -> List[List[int]]:
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        result = []

        for i in range(n - 2):
            if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
                continue

            left, right = i + 1, n - 1

            while left < right:
                current_sum = sorted_nums[i] + sorted_nums[left] + sorted_nums[right]

                if current_sum == 0:
                    result.append([sorted_nums[i], sorted_nums[left], sorted_nums[right]])
                    while left < right and sorted_nums[left] == sorted_nums[left + 1]:
                        left += 1
                    while left < right and sorted_nums[right] == sorted_nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif current_sum < 0:
                    left += 1
                else:
                    right -= 1

        return result


# ============= TEST CASES =============
solution = Solution()
print(solution.threeSum([-1, 0, 1, 2, -1, -4]))           # [[-1, -1, 2], [-1, 0, 1]]
print(solution.threeSum([0, 0, 0]))                       # [[0, 0, 0]]
print(solution.threeSum([0, 0, 0, 0]))                    # [[0, 0, 0]]
print(solution.threeSum([1, 2, 3]))                       # []
print(solution.threeSum([]))                              # []
print(solution.threeSum([-2, 0, 1, 1, 2]))                # [[-2, 0, 2], [-2, 1, 1]]
print(solution.threeSum([3, 0, -2, -1, 1, 2]))            # [[-2, -1, 3], [-2, 0, 2], [-1, 0, 1]]
print(solution.threeSum([-2, -1, -1, 0, 0, 1, 1, 2]))     # [[-2, 0, 2], [-2, 1, 1], [-1, -1, 2], [-1, 0, 1]]
```

---

## 5. Pitfalls That Cost Time in Practice

| Trap | What goes wrong | Fix |
|---|---|---|
| **Index vs value** | `current_sum = i + sorted_nums[L] + sorted_nums[R]` adds the position `i` instead of `sorted_nums[i]`. | Always wrap indices: `sorted_nums[i]`. |
| **`range(j + i, n)` typo** | Looks like `j + 1` but is wrong when `i ≥ 2`. Silently skips triplets. | Type `j + 1` slowly. Read it back. |
| **`set().add()` returns None** | `seen = set().add(x)` → `seen` is `None`. | Call `.add()` on its own line, don't assign. |
| **List in a set** | `set.add([1,2,3])` → TypeError, unhashable. | Wrap: `tuple([1,2,3])`. |
| **Pointers outside outer loop** | Second anchor starts with stale L, R. | Reset `left, right = i+1, n-1` INSIDE the loop. |
| **Match branch doesn't move pointers** | With proper `elif`, the match branch is isolated. Without explicit `left += 1; right -= 1`, infinite loop. | Always advance both pointers in the match branch. |
| **Missing `i > 0` guard** | `sorted_nums[-1]` silently returns the last element. Wrong comparison. | Guard the skip check: `if i > 0 and ...`. |
| **`if` vs `elif`** | Two separate `if`s let the match branch fall through into the `< 0` check. Set saves you, but the inner loop does extra work. | Chain as `if / elif / else`. |

---

## Interview Out-Loud

> "I'd state the brute force first: three nested loops, O(n³). At n=3000 that's about 4.5 billion operations — too slow.
> The optimal is sort plus two pointers. Sorting is O(n log n) but unlocks two benefits: it lets me reason about the two-pointer sum direction, AND it groups duplicates next to each other so I can skip them by checking adjacent positions.
> The outer loop fixes one element as the anchor. For each anchor I run a two-pointer scan over the rest, looking for L + R = -anchor. That's essentially LC 167 with a fixed target.
> To prevent duplicate triplets, I add three skip checks: skip the outer anchor if it matches the previous anchor's value, and after each match walk L and R past their duplicate neighbors before advancing.
> Total time O(n²), space O(1) auxiliary. The skips guarantee uniqueness, so no set is needed."

---

## Likely Follow-ups

The interview is one question that grows in parts — 3Sum has two natural directions to grow.

- **"Now find the triplet whose sum is CLOSEST to a target."** → Same sort + anchor + two-pointer skeleton, but track the best distance instead of deduping. That is LC 16 3Sum Closest — the next script in this chain.
- **"Generalize to four numbers — or k numbers."** → 4Sum adds one more anchor loop around this code (O(n³)). For general k, recurse: peel anchors until two remain, then run the two-pointer scan.
- **"COUNT the triplets instead of listing them."** → Don't skip duplicates — count the sizes of equal-value runs at L and R and multiply, instead of recording one triplet.
- **"What if the target isn't zero?"** → Nothing structural changes: look for `L + R = target - anchor` instead of `-anchor`.

---

## 7. Chain Position

This problem sits in the **two-pointer chain**:

`LC 1 Two Sum (unsorted, hash map)` → `LC 167 Two Sum II (sorted, two-pointer)` → **`LC 15 3Sum`** → `LC 16 3Sum Closest` → (later: `LC 18 4Sum`)

Every problem in the chain reuses the previous one's skeleton. 3Sum is the keystone — if you know this cold, 3Sum Closest takes 15 minutes and 4Sum takes 25.

---

**You now have a complete, professional 3Sum practice script.** Read out loud, retype tomorrow morning from memory, then run the test cases.
