# LC 53 — Maximum Subarray · Practice Script

**Problem:**  
Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Subarray means contiguous, right? Not a subsequence?"** — Contiguous. A subsequence (skipping allowed) would just be "sum all positives" — a different problem.
- **"Can the subarray be empty?"** — No, at least one element. So an all-negative array returns the least negative number, NOT 0.
- **"What if every number is negative?"** — Return the largest single element. This is why you initialize to `nums[0]`, never to 0.
- **"Do you want the sum, or the subarray itself?"** — The sum. Returning the subarray needs start/end index tracking on top of Kadane's.
- **"Can the input be empty?"** — Constraints say no, but agree on a return value (0 or an error) in one sentence.

---

## Solution 1: Brute Force (Two Nested Loops)

```python
from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]

        for i in range(len(nums)):
            current_sum = 0
            for j in range(i, len(nums)):
                current_sum += nums[j]
                if current_sum > max_sum:
                    max_sum = current_sum

        return max_sum
```

**Time Complexity:** O(n²)  
**Space Complexity:** O(1)

### Why this is NOT recommended:
- Too slow for large inputs (can be up to 10,000 elements).
- Interviewers expect the much faster O(n) solution.
- Does not demonstrate the key insight of Kadane’s Algorithm.

---

## Solution 2: Optimal (Kadane’s Algorithm) — Recommended

```python
from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        max_current = max_global = nums[0]

        for num in nums[1:]:
            max_current = max(num, max_current + num)
            max_global = max(max_global, max_current)

        return max_global
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

### Trace on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| i | num | max_current = max(num, prev + num) | max_global |
|---|-----|------------------------------------|------------|
| 0 | -2  | -2 (init)                          | -2         |
| 1 |  1  | max(1, -2+1=-1) = **1**            |  1         |
| 2 | -3  | max(-3, 1+-3=-2) = **-2**          |  1         |
| 3 |  4  | max(4, -2+4=2) = **4** (reset)     |  4         |
| 4 | -1  | max(-1, 4+-1=3) = **3**            |  4         |
| 5 |  2  | max(2, 3+2=5) = **5**              |  5         |
| 6 |  1  | max(1, 5+1=6) = **6**              |  6         |
| 7 | -5  | max(-5, 6+-5=1) = **1**            |  6         |
| 8 |  4  | max(4, 1+4=5) = **5**              |  6         |

Result: `6` from subarray `[4, -1, 2, 1]`. Watch row 3 — the running sum was negative, so Kadane resets to `num` instead of extending. That's the whole trick.

### Why this is RECOMMENDED:
- Runs in linear time — very efficient.
- Classic example of dynamic programming / greedy thinking.
- Shows you can make smart decisions at each step ("continue or reset").
- Very common pattern in interviews.

---

## Comparison

| Aspect                    | Brute Force          | Kadane’s Algorithm     | Winner          |
|---------------------------|----------------------|------------------------|-----------------|
| Time Complexity           | O(n²)                | **O(n)**               | Kadane          |
| Space Complexity          | O(1)                 | O(1)                   | Tie             |
| Interview Signal          | Weak                 | **Strong**             | Kadane          |
| Ease of Explanation       | Easy                 | Medium                 | Brute Force     |
| Real-world Performance    | Poor                 | Excellent              | Kadane          |

---

## Interview Out-Loud

> "The brute force approach checks every possible subarray using two nested loops, which is O(n²).  
> Instead, I can use Kadane’s Algorithm. At every position, I decide whether to continue the current subarray or start fresh from the current number.  
> I keep track of the best sum seen so far. This way we solve it in O(n) time and O(1) space."

---

## Test Cases

| Input                          | Output | Explanation |
|--------------------------------|--------|-------------|
| `[-2,1,-3,4,-1,2,1,-5,4]`      | 6      | Subarray `[4,-1,2,1]` |
| `[1]`                          | 1      | Single element |
| `[5,4,-1,7,8]`                 | 23     | Entire array |
| `[-1]`                         | -1     | Negative number |
| `[-2,-1]`                      | -1     | Best is the least negative |

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Initializing `max_global = 0` | All-negative arrays return 0 instead of the largest (least negative) | Initialize to `nums[0]`, not 0 |
| Resetting `max_current` to 0 instead of `num` | Misses arrays of all negatives | `max_current = max(num, max_current + num)` — picks the bigger of "extend" vs "restart at num" |
| Iterating from index 0 with the standard pattern | Double-counts `nums[0]` if you initialize `max_current = nums[0]` and loop from index 0 | Start the loop at index 1 (`for num in nums[1:]`) |
| Returning `max_current` instead of `max_global` | Returns the LAST running sum, not the BEST seen | Always return `max_global` |
| Confusing "subarray" with "subsequence" | Subarrays are CONTIGUOUS; subsequences can skip | Read the problem — Kadane's is for subarrays only |

---

## Likely Follow-ups

The interview is one question that grows in parts — Kadane's is the base, then they bend it.

- **"Return the subarray itself, not just the sum."** → Remember a `start` index every time Kadane resets; save `(start, i)` whenever `max_global` improves.
- **"Now it's the maximum PRODUCT subarray."** → Negatives flip signs, so track BOTH the max and min product ending here; a negative number swaps them.
- **"The array is circular — it can wrap around."** → Best of: normal Kadane, or total sum minus the MINIMUM subarray (the wrap case). Watch the all-negative edge case.
- **"What's the brute force and why is yours better?"** → Two nested loops sum every subarray, roughly n²/2 sums. Kadane's makes one decision per element in a single pass.

---

## Chain position

Maximum Subarray is **Kadane's algorithm** — the simplest "running optimum with reset" pattern. The "extend or restart" idea extends to:
- **Best Time to Buy/Sell** — same shape (best ending here vs restart)
- **Maximum Product Subarray** — same one-pass with two trackers (min + max, because of negatives)
- **Maximum Sum Circular Subarray** — Kadane's + Kadane's on the inverse
- **House Robber** — same DP shape: at each step, take or skip

Kadane's is the gateway to dynamic programming. The "decision at each step" insight is reused dozens of times in harder problems.