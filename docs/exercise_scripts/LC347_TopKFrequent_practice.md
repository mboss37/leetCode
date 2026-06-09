# LC 347 — Top K Frequent Elements · Practice Script

---

## Problem

> Given an integer array `nums` and an integer `k`, return the **k most frequent elements**. You may return the answer in any order.
>
> Your algorithm's time complexity must be **better than O(n log n)**.

**Constraints:**
- `1 <= nums.length <= 10⁵`
- `-10⁴ <= nums[i] <= 10⁴`
- `1 <= k <= number of unique elements`
- The answer is **unique** (no ambiguity at the boundary).

**Key constraint:** *"better than O(n log n)"* rules out a full sort.

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"If two elements tie in frequency at the k boundary, which do I pick?"** — Spec guarantees the answer is unique, so no ties at the cut. Without that guarantee, ask for a tie-break rule.
- **"Is k always valid — at most the number of unique elements?"** — Yes, guaranteed. No need to handle k being too big.
- **"Return just the elements, or the elements with their counts?"** — Just the elements, any order.
- **"Is 'better than O(n log n)' a hard requirement?"** — Yes. A full sort is rejected; O(n log k) or O(n) both pass.

---

## 1. Verbal baseline (state only, don't write) — Sort by count, O(n log n)

> *"Brute force is `Counter(nums)` then sort the items by count, take the top k. That's O(n log n) — sort dominates. Spec requires better than O(n log n), so this would be rejected."*

You **state this verbally** in the interview, then move on. Don't write it as code.

---

## 2. RECOMMENDED — `Counter.most_common(k)` (~10 lines)

```python
from collections import Counter
from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)
        top_pairs = counts.most_common(k)
        result = []
        for num, count in top_pairs:
            result.append(num)
        return result
```

### Why this is the right starting answer

Python's `Counter.most_common(k)` is **purpose-built** for this exact problem. Internally it runs a **min-heap of size k** — the same algorithm an interviewer would want to see.

- **Time:** O(n log k)
- **Space:** O(n) for the Counter
- **Spec passes** (O(n log k) is better than O(n log n) when k < n).

### What `most_common(k)` returns

A list of `(item, count)` tuples, already sorted from most-frequent to least-frequent:
```python
Counter([1, 1, 1, 2, 2, 3]).most_common(2)
# → [(1, 3), (2, 2)]
```

### What the `for num, count` loop does

> Each tuple in `top_pairs` is unpacked: `num` gets the first element, `count` gets the second. We only need `num`, but naming both makes intent clear.

If you prefer no unpacking:
```python
for pair in top_pairs:
    result.append(pair[0])
```

---

## FOLLOW-UP — Manual min-heap (only if asked "without most_common")

```python
import heapq
from collections import Counter
from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)
        heap = []
        for num, count in counts.items():
            heapq.heappush(heap, (count, num))
            if len(heap) > k:
                heapq.heappop(heap)
        result = []
        for count, num in heap:
            result.append(num)
        return result
```

### How the heap idea works

> Maintain a heap of size k holding the k most-frequent items seen so far. The heap is a **min-heap** (Python default), so its root is the SMALLEST count in the heap. If a new item has a count BIGGER than the root, the root deserves to be evicted → `heappop`. Pushing then popping if too big keeps the heap at size k.

After processing all items, the heap holds exactly the k most-frequent.

- **Tuple order:** `(count, num)` — heap compares by count first, which is what we want.
- **Time:** O(n log k) — push/pop on a size-k heap is O(log k), times n items.
- **Space:** O(n + k).

### When to write this

Only when the interviewer says *"now do it without using `most_common`."* Otherwise lead with the recommended version.

---

## 4. BONUS — Bucket sort by frequency, O(n)

Truly linear time. Build an array indexed by frequency, walk it from high to low:

```python
from collections import Counter
from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)
        n = len(nums)
        # buckets[freq] = list of numbers with that frequency
        buckets = [[] for _ in range(n + 1)]
        for num, count in counts.items():
            buckets[count].append(num)
        # Walk from highest frequency down, collecting numbers until we have k
        result = []
        for freq in range(n, 0, -1):
            for num in buckets[freq]:
                result.append(num)
                if len(result) == k:
                    return result
        return result
```

- **Time:** O(n) — no sorting, no heap.
- **Space:** O(n) for the buckets.
- This is the **truly linear** solution. Most elegant if you spot it under pressure.
- Reasonable to show if you have time, but the heap version is the more commonly expected answer.

---

## 5. Comparison

| Approach | Time | Space | Lines | Interview Verdict |
|---|---|---|---|---|
| Sort by count (verbal baseline) | O(n log n) | O(n) | ~5 | ✗ Spec rejected |
| **`Counter.most_common(k)`** | **O(n log k)** | O(n) | ~10 | **✓ Lead with this** |
| Manual min-heap | O(n log k) | O(n+k) | ~15 | ✓ Follow-up if asked |
| Bucket sort | **O(n)** | O(n) | ~15 | ✓ Bonus if you spot it |

---

## 6. Trace `Counter.most_common` on `[1, 1, 1, 2, 2, 3]`, k = 2

| Step | What happens |
|---|---|
| `counts = Counter(nums)` | `{1: 3, 2: 2, 3: 1}` |
| `most_common(2)` | `[(1, 3), (2, 2)]` — already sorted by count desc |
| Loop, extract num | `result = [1, 2]` |

---

## 7. How to Practice

### Step 1: Read out loud

> "Spec says better than O(n log n), so a full sort is out. I'll use `Counter(nums).most_common(k)` — Python's standard library does this in O(n log k) using a min-heap internally.
>
> Counter builds the frequency map in O(n). most_common(k) returns the k most-frequent as a list of (number, count) tuples. I unpack and return just the numbers.
>
> If you want me to implement this without most_common, I'd build the heap manually — heappush each (count, number) tuple, pop when the heap exceeds size k. Same big-O, just more code.
>
> If you want true O(n), there's a bucket-sort approach: index numbers by their frequency in an array, walk from highest frequency down until we've collected k."

### Step 2: Key Points

- **Don't write the sort baseline.** State it verbally only.
- **Lead with `most_common(k)`.** It's the stdlib answer.
- **Know two follow-ups** in your pocket: manual heap (O(n log k)) and bucket sort (O(n)).
- **Order doesn't matter** in the output — the spec says "in any order."

### Step 3: Test Cases

| nums                       | k | Expected (any order) | Notes |
|----------------------------|---|----------------------|-------|
| `[1, 1, 1, 2, 2, 3]`       | 2 | `[1, 2]`             | Canonical |
| `[1]`                      | 1 | `[1]`                | Single element |
| `[1, 2, 2, 3, 3, 3]`       | 3 | `[3, 2, 1]`          | All elements returned |
| `[4, 4, 4, 4, 5, 5, 6]`    | 1 | `[4]`                | One winner |
| `[-1, -1, 0, 0, 1, 1]`     | 2 | any 2 of [-1, 0, 1]  | All tied → any 2 |

---

## 8. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Dict-flip (count → number) | Collisions overwrite when counts tie | Use Counter directly; never flip |
| `sorted(counts.items())` | Sorts by KEY (the number), not count | Always specify `key=` for sort |
| Heap with `(num, count)` order | Heap compares by num first — wrong | Use `(count, num)` so count is compared first |
| Forgetting `heappop` after push | Heap grows beyond k → wrong time complexity | Pop after every push when `len(heap) > k` |
| Returning the tuples directly | Spec wants list of numbers | Unpack and extract `num` |

---

## 9. Interview Out-Loud Explanation

> "Spec requires better than O(n log n), so a full sort is out. I'll use `Counter.most_common(k)` from the standard library — O(n log k) internally via a min-heap, exactly the right complexity.
>
> Count frequencies with `Counter(nums)`. Call `most_common(k)` to get the k most-frequent as (number, count) tuples already sorted. Loop through and extract just the numbers.
>
> Time: O(n log k). Space: O(n) for the Counter.
>
> If asked to implement without `most_common`, I'd build the heap manually: push each (count, number) tuple, pop when the heap exceeds size k. If asked for true O(n), I'd use bucket sort — index numbers by frequency, walk from the highest bucket down."

---

## Likely Follow-ups

The interview is one question that grows in parts — the k-variants here are almost guaranteed.

- **"Now without `most_common`."** → The manual size-k min-heap — already written above in this script.
- **"Can you do true O(n)?"** → Bucket sort by frequency — the bonus section above.
- **"Top k frequent WORDS, ties broken alphabetically."** → Heap of `(-count, word)` tuples — negate the count so the heap orders by count descending, word ascending.
- **"The numbers arrive as a stream — top k at any moment?"** → Keep the Counter updated per element; recompute the size-k heap on demand, or maintain it incrementally.

---

**Chain position:** Top K Frequent is the **heap intro**. The pattern extends to:
- **Kth Largest Element** — same shape, return just one element.
- **K Closest Points to Origin** — heap of size K by distance.
- **Find Median from Data Stream** — two heaps (DROPPED from this prep as Hard-tier; pattern still in cheatsheet).
