# LC 34 — Find First and Last Position of Element in Sorted Array · Practice Script

**Chain:** Binary Search → Search Insert Position → **Find First and Last Position**

---

## Problem

> Given a **sorted** (ascending) array of integers `nums` and a `target` value, return the **first and last positions** of `target` as a list `[first, last]`. If `target` is not found, return `[-1, -1]`.
>
> You must write an algorithm with **O(log n) runtime complexity**.

**Constraints:**
- `0 <= nums.length <= 10⁵`
- `-10⁹ <= nums[i] <= 10⁹`
- `nums` is sorted ascending
- **Values can REPEAT** (this is the twist)
- `-10⁹ <= target <= 10⁹`

**Key fact:** plain Binary Search returns SOME index where target appears — but with duplicates, you need the leftmost AND rightmost positions. **Two binary searches**, each biased to one side.

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Can the array be empty?"** — Yes, length can be 0. Both helpers start `result = -1`, so `[-1, -1]` falls out for free.
- **"Duplicates are allowed, right?"** — Yes — that's the whole twist. Without duplicates this is plain Binary Search.
- **"If the target appears exactly once, do I return the same index twice?"** — Yes, `[i, i]`.
- **"Is O(log n) required?"** — Yes. The one-pass linear scan is correct but rejected.

---

## 1. Linear Scan — NOT RECOMMENDED (O(n))

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        first = -1
        last = -1
        for i, num in enumerate(nums):
            if num == target:
                if first == -1:
                    first = i
                last = i
        return [first, last]
```

- **Time:** O(n)
- **Space:** O(1)
- Single pass: set `first` only the first time you hit target, always update `last`.
- **Rejected in interview** — spec requires O(log n).

---

## 2. Two Biased Binary Searches — RECOMMENDED (O(log n))

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def find_left(nums, target):
            left, right = 0, len(nums) - 1
            result = -1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] == target:
                    result = mid
                    right = mid - 1      # keep narrowing LEFT
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return result

        def find_right(nums, target):
            left, right = 0, len(nums) - 1
            result = -1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] == target:
                    result = mid
                    left = mid + 1       # keep narrowing RIGHT
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return result

        return [find_left(nums, target), find_right(nums, target)]
```

### The key insight

Plain Binary Search returns `mid` the moment it finds a match. **This version DOESN'T stop on a match.** Instead it:
1. **Records** the matching index in `result`.
2. **Keeps narrowing** in a biased direction to find an even better match.

For `find_left`: on match, narrow RIGHT (`right = mid - 1`) — keep looking for earlier matches.
For `find_right`: on match, narrow LEFT (`left = mid + 1`) — keep looking for later matches.

The two helpers are **identical except for that one line** on the `==` branch.

### Trace on `[5, 7, 7, 8, 8, 10]`, target = 8

**find_left:**

| step | L | R | mid | nums[mid] | branch | result |
|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 2 | 7 | < 8 → L = 3 | — |
| 2 | 3 | 5 | 4 | 8 | **==** → record 4, **R = 3** | 4 |
| 3 | 3 | 3 | 3 | 8 | **==** → record 3, **R = 2** | 3 |
| 4 | L > R → exit |

Returns `3`.

**find_right:**

| step | L | R | mid | nums[mid] | branch | result |
|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 2 | 7 | < 8 → L = 3 | — |
| 2 | 3 | 5 | 4 | 8 | **==** → record 4, **L = 5** | 4 |
| 3 | 5 | 5 | 5 | 10 | > 8 → R = 4 | 4 |
| 4 | L > R → exit |

Returns `4`.

**Result: `[3, 4]`** ✓

### Complexity

- **Time:** O(log n) — two binary searches, each O(log n). Constant 2 drops out: O(log n).
- **Space:** O(1) — only a few index variables.

---

## 3. Comparison

| Aspect              | Linear (O(n))         | Two Binary Searches (O(log n)) | Winner       |
|---------------------|------------------------|---------------------------------|--------------|
| Time                | O(n)                   | **O(log n)**                    | Binary       |
| Space               | O(1)                   | O(1)                            | Tie          |
| Uses sorted?        | No                     | **Yes**                         | Binary       |
| Lines of code       | ~7                     | ~25                             | Linear       |
| Accepted by spec?   | No                     | **Yes**                         | Binary       |

---

## 4. How to Practice This Script

### Step 1: Read out loud (1 min)

> "Plain Binary Search returns the FIRST index it lands on where the value equals target. But duplicates can sit on either side of that mid, so I need to find the leftmost AND rightmost separately.
>
> Two binary searches. Each is plain Binary Search with ONE change: on a match, instead of returning immediately, I record the index and keep narrowing in a biased direction.
>
> For leftmost: on match, narrow right (`right = mid - 1`).
> For rightmost: on match, narrow left (`left = mid + 1`).
>
> Return `[find_left(), find_right()]`. Both default to `-1` if no match exists.
>
> Time O(log n), space O(1)."

### Step 2: Key Points

- **Don't return on match — record and keep narrowing.** The single most important idea.
- **Two helpers**, identical except for the `==` branch direction.
- **Each helper returns -1 if no match** — the result variable starts at -1.
- The skeleton is **plain Binary Search**, just don't short-circuit.

### Step 3: Test Cases

| nums                          | target | Expected | Notes                          |
|-------------------------------|--------|----------|--------------------------------|
| `[5, 7, 7, 8, 8, 10]`         | 8      | `[3, 4]` | Canonical                      |
| `[5, 7, 7, 8, 8, 10]`         | 6      | `[-1,-1]`| Not in array                   |
| `[]`                          | 0      | `[-1,-1]`| Empty array                    |
| `[1]`                         | 1      | `[0, 0]` | Single element, match          |
| `[1]`                         | 0      | `[-1,-1]`| Single element, no match       |
| `[2, 2]`                      | 2      | `[0, 1]` | All match                      |
| `[1, 2, 3, 3, 3, 3, 3, 4, 5]` | 3      | `[2, 6]` | Wide matching block (5 wide)   |

---

## 5. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Returning `mid` on match (plain Binary Search) | Gets ONE valid index but not the leftmost/rightmost | Record and keep narrowing |
| Trying adjacency check (`nums[mid-1] == target`) | Breaks on blocks wider than 2; also needs bounds guard | Don't — use the biased binary search instead |
| `result = -1` initialization | Required so "not found" returns -1 cleanly | Set `result = -1` before the loop |
| Forgetting parens on `mid` | `left + right // 2` parses as `left + (right // 2)` | Use `(left + right) // 2` |
| `while left < right` instead of `<=` | Misses single-element check | Use `<=` |

---

## 6. Interview Out-Loud Explanation

> "Plain Binary Search returns the first index it lands on where the value equals target. But duplicates can sit on either side of that, so I need two passes — one biased left, one biased right.
>
> Each pass is plain Binary Search with one tweak: on a match, instead of returning, I record the index and keep narrowing in a biased direction. For the leftmost: narrow right after a match. For the rightmost: narrow left after a match.
>
> Both helpers default to `-1` if no match exists. Return `[find_left(), find_right()]`.
>
> O(log n) for each search, two searches, still O(log n). O(1) space."

---

## Likely Follow-ups

The interview is one question that grows in parts — these are the natural extensions once both searches work.

- **"How many times does the target appear?"** → `last - first + 1` when found, 0 otherwise. No extra search needed.
- **"Can you do it with the standard library?"** → `bisect_left` gives the first position, `bisect_right - 1` gives the last. Check the value at `bisect_left` actually equals target.
- **"What if the array was rotated at an unknown point?"** → Search in Rotated Sorted Array (LC 33): find which half is sorted, then narrow.
- **"Count how many numbers fall in a range [lo, hi]."** → Same biased searches: leftmost position of `lo`, rightmost of `hi`, subtract.

---

**Chain position:** This is the "biased binary search" pattern. It extends to:
- **Search in Rotated Sorted Array** — adds pivot detection
- **Find Peak Element** — biased toward the peak

Master this one — the "record-and-keep-narrowing" idea is reused.
