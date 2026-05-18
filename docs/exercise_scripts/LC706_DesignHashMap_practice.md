# LC 706 — Design HashMap · Practice Script

---

## Problem

> Design a HashMap without using any built-in hash table libraries:
> - `put(key, value)` — insert or update
> - `get(key)` — return value, or `-1` if not present
> - `remove(key)` — remove the mapping
>
> Keys and values: `0 <= key, value <= 10⁶`. Up to 10⁴ calls.

---

## The pattern — separate chaining

Buckets array of size `M`. Each bucket is a list of `(key, value)` pairs.

To put/get/remove key `k`:
1. **Hash:** `i = k % M`. (`%` is the simplest hash you can write.)
2. **Bucket lookup:** scan `buckets[i]` for matching key.

If hashing distributes keys evenly and each bucket stays small → average **O(1)**.

```
buckets [0]  → [(1, 100), (1001, 50)]
        [1]  → [(2, 999)]
        [2]  → []
        ...
        [M-1]→ [(M-1, 42)]
```

---

## No meaningful brute force

Design problem — implement a hash map without using one. The naive alternative (a flat list of `(key, value)` pairs, O(n) per lookup) violates the implicit performance contract of "hash map". The separate-chaining structure below is the minimal correct answer that delivers average O(1).

---

## RECOMMENDED — Separate Chaining, Fixed Bucket Count

```python
class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _bucket(self, key):
        return self.buckets[key % self.size]

    def put(self, key, value):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```

### Why 1000 buckets?

LeetCode's spec allows ≤10⁴ calls. With 1000 buckets, the average bucket holds ≤10 entries → scan is essentially constant in practice.

In real systems you'd:
- Pick `M` as a **prime number** (better key distribution).
- **Resize** (rehash to a bigger array) when load factor (entries / M) exceeds a threshold.

For interview: state these as known improvements, don't implement them unless asked.

### Complexity

| op | Average | Worst case |
|---|---|---|
| put / get / remove | O(1) | O(n) — if all keys collide into one bucket |
| **Space** | O(n + M) | |

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Storing only values, not (key, value) | Two different keys hash to the same bucket and you can't tell them apart | Always store both |
| Forgetting to check "key already exists" in `put` | Duplicate entries → `get` returns first hit, but state is corrupt | Scan first, update in place |
| Picking `M = 1` (or too small) | Every key collides → O(n) per op | Reasonable `M` (e.g. 1000) |
| Returning None instead of -1 on missing key | Wrong return contract | `return -1` |

---

## Interview Out-Loud

> "Separate chaining. Buckets array of fixed size — say 1000. Each bucket is a list of (key, value) tuples.
>
> Hash with `key % size`. To put: walk the bucket to update if key exists, else append. To get: scan the bucket, return value or -1. To remove: scan and pop.
>
> Average O(1) per op when keys distribute well. Worst case O(n) if everything collides.
>
> Real implementations would use a prime modulus and resize when the load factor gets high — happy to add either if you'd like."

---

**Chain position:** Foundational data structure design. Same primitive underlies: Design HashSet, LRU Cache (paired with DLL).
