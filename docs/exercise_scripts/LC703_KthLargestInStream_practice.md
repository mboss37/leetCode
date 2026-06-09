# LC 703 — Kth Largest Element in a Stream · Practice Script

---

## Problem

> Design a class that finds the **k-th largest** element in a stream of integers.
>
> - `KthLargest(k, nums)` initializes the object with `k` and an initial list of numbers.
> - `add(val)` appends `val` to the stream and returns the k-th largest value seen so far.

**Constraints:**
- `1 <= k <= 10⁴`
- `0 <= nums.length <= 10⁴`
- `-10⁴ <= val, nums[i] <= 10⁴`
- At least k+1 values are guaranteed before the first `add` call when `nums` is empty.
- At most 10⁴ calls to `add`.

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Do duplicates count separately? Stream [5,5,4], k=2 — is the answer 5?"** — Yes, 5. K-th largest counts positions, not distinct values.
- **"Can the initial list have fewer than k elements, or be empty?"** — Yes. The heap just fills up over the first adds; only pop when size exceeds k.
- **"Is add ever called before k values exist?"** — No — the spec guarantees k values before an answer is needed.
- **"Must I keep the whole stream in memory?"** — No. Only the top k values matter — that's the size-k heap insight.
- **"Can values be negative?"** — Yes, down to -10⁴. Nothing changes.

---

## No meaningful brute force

The naive approach is *"on every add, sort the entire array and return index k-1"* → **O(n log n) per call**. Doable but wasteful — we don't actually need a fully sorted array, only the k-th largest.

A **min-heap of size k** keeps just the top-k values in the stream. Add is O(log k), peek is O(1). Net: O(log k) per call instead of O(n log n).

---

## RECOMMENDED — Min-Heap of size k (O(log k) per call)

```python
import heapq
from typing import List

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = nums                     # use the input list directly
        heapq.heapify(self.heap)             # turn it into a min-heap in O(n)
        while len(self.heap) > k:
            heapq.heappop(self.heap)         # shrink to size k by dropping smallest

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)         # keep heap at size k
        return self.heap[0]                  # smallest of top-k = k-th largest overall
```

### The key insight

A **min-heap of size k** holds exactly the **k largest values** seen so far. The root of that heap (smallest of the top-k) IS the k-th largest overall.

When a new value arrives:
- If it's small enough that it doesn't belong in the top-k → it gets pushed in, then immediately popped out (still O(log k)).
- If it's bigger than at least one of our current top-k → it pushes the smallest one out.

Either way, after the dust settles, `heap[0]` (the new minimum of the top-k) is the answer.

### Why a min-heap and not a max-heap?

We want to **eject the smallest** of our current top-k whenever a bigger value arrives. The smallest is at the root of a min-heap → O(log k) pop. A max-heap would have its smallest buried somewhere at the bottom → O(k) to find.

The mental flip is worth pinning: *"to track the k LARGEST, use a MIN-heap of size k."* The min-heap's root is the cut-off value — anything smaller doesn't qualify for top-k.

### Trace on `k = 3, nums = [4, 5, 8, 2]`, then add(3), add(5), add(10), add(9), add(4)

After init:
- heapify `[4, 5, 8, 2]` → `[2, 4, 8, 5]` (heap order — root is min)
- Length 4 > k=3 → pop the root (2). Heap = `[4, 5, 8]`. Top-3 so far.

| call | val | heap before push | after push | size > k? pop | heap after | k-th largest |
|---|---|---|---|---|---|---|
| add(3) | 3 | [4, 5, 8] | [3, 4, 8, 5] | yes → pop 3 | [4, 5, 8] | **4** |
| add(5) | 5 | [4, 5, 8] | [4, 5, 8, 5] | yes → pop 4 | [5, 5, 8] | **5** |
| add(10) | 10 | [5, 5, 8] | [5, 5, 8, 10] | yes → pop 5 | [5, 8, 10] | **5** |
| add(9) | 9 | [5, 8, 10] | [5, 8, 10, 9] | yes → pop 5 | [8, 9, 10] | **8** |
| add(4) | 4 | [8, 9, 10] | [4, 8, 10, 9] | yes → pop 4 | [8, 9, 10] | **8** |

(Heap-order arrays may shuffle internally — what matters is the root is always the min of the top-3.)

### Complexity

- **Init:** O(n + (n−k) log n) = effectively O(n log n) worst case.
- **Add:** O(log k) per call.
- **Space:** O(k) — heap never exceeds size k after init.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Using a max-heap | Smallest of top-k buried at the bottom — can't pop in O(log k) | Use a **min-heap** of size k |
| Forgetting `heapq.heapify` | Treating an unordered list as a heap → wrong answers | `heapify` on the input first |
| Returning `self.heap[-1]` | Heap order ≠ sorted order — last index is NOT the largest | `self.heap[0]` (the root, which is the min of top-k) |
| Letting heap grow past k | O(log n) per call instead of O(log k); and `heap[0]` is no longer the k-th largest | Pop after every push when `len > k` |
| Initializing heap with one element popped per loop, manually | Reinventing `heapify` — slower and verbose | `heapify(self.heap)` then prune to size k |

---

## Alternative — `heapq.heappushpop` (one-liner combo)

Slightly cleaner:

```python
def add(self, val: int) -> int:
    if len(self.heap) < self.k:
        heapq.heappush(self.heap, val)
    elif val > self.heap[0]:
        heapq.heappushpop(self.heap, val)    # push then pop in one O(log k) op
    return self.heap[0]
```

`heappushpop(heap, val)` pushes `val`, then pops the smallest, in a single combined operation. Slightly faster than separate push + pop. Either form is fine in interviews.

---

## Interview Out-Loud

> "Min-heap of size k. The root of that heap is the k-th largest overall — anything smaller has already been pushed out.
>
> On init: heapify the input, then pop until size k. On add: push the new value, pop if size exceeded k, return the root.
>
> O(log k) per add — we don't track values that can never make the top-k. Stdlib `heapq` is a min-heap, so for top-k LARGEST we want exactly that. If the problem asked for k-th smallest, we'd flip to a max-heap by negating values on push/pop."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect one of these next:

- **"K-th SMALLEST instead of largest?"** → Flip the heap: negate values on push and pop, so Python's min-heap behaves as a max-heap of size k.
- **"K-th largest of a STATIC array, one query?"** → LC 215. Same size-k heap in O(n log k), or quickselect for average O(n).
- **"Find the MEDIAN of the stream?"** → LC 295. Two heaps: max-heap for the lower half, min-heap for the upper half, kept balanced.
- **"Top k most FREQUENT elements?"** → LC 347 — there's a practice script for it in this repo. Count first, then the same size-k heap over frequencies.

---

**Chain position:** Heap pattern. Same idea in: **Top K Frequent Elements** (Phase A — `Counter.most_common(k)` uses this internally), **Find K Closest Points to Origin**, **K Closest Numbers in Stream**, **Last Stone Weight**.

The reflex: *"k-th largest / smallest / closest in a stream"* → reach for a size-k heap.
