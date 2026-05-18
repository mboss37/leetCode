# LC 146 — LRU Cache · Practice Script

---

## Problem

> Design an LRU (Least Recently Used) cache.
>
> - `LRUCache(capacity)` — initializes the cache with a positive size limit.
> - `get(key) → int` — returns the value for `key` if present, else `-1`. Marks `key` as most recently used.
> - `put(key, value)` — inserts or updates the value. If insertion exceeds capacity, evicts the LRU.
>
> Both must run in **O(1) average time**.

**Constraints:**
- `1 <= capacity <= 3000`
- `0 <= key <= 10⁴`, `0 <= value <= 10⁵`
- At most `2 × 10⁵` total calls.

**Key requirement:** O(1) for both operations. This is the famous design problem.

---

## 1. RECOMMENDED — `collections.OrderedDict` (~15 lines)

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

### Why this is the right starting answer

Python's `OrderedDict` IS a hash map + linked list internally. It already provides O(1) "move to end" and O(1) "pop from front." **You don't have to rebuild what Python already shipped.**

Using `OrderedDict` shows:
- Pythonic instincts (using the right stdlib tool).
- O(1) understanding (you know why `move_to_end` and `popitem` are O(1)).
- Code that's readable in 15 lines instead of 50.

### How it maps to the LRU semantics

- **Order in the OrderedDict** = order of last access. Front = oldest. End = most recent.
- **`move_to_end(key)`** — promote a key to most-recent position on access.
- **`popitem(last=False)`** — evict from the front (oldest) on capacity overflow.

### Trace `put(1,1) put(2,2) get(1) put(3,3) get(2)`

| op | cache (front → end) | returns |
|---|---|---|
| put(1,1) | {1: 1} | — |
| put(2,2) | {1: 1, 2: 2} | — |
| get(1) | {2: 2, 1: 1} | 1 |
| put(3,3) | {1: 1, 3: 3} | — (capacity exceeded → evicted 2 from front) |
| get(2) | (same) | -1 |

### Complexity

- **Time:** O(1) per `get` and `put`.
- **Space:** O(capacity).

---

## 2. FOLLOW-UP (if asked) — manual hash map + doubly-linked list

If the interviewer says *"now do it without `OrderedDict`"*, you fall back to building the structure manually.

```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_head(node)
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

### Why this version is bigger but same big-O

- **Node class** — each cache entry wraps in an object that carries `prev` and `next` pointers, so you can splice it out of the middle of the list in O(1).
- **Sentinel `head` and `tail`** — dummy nodes that always exist, removing all "empty list" edge cases. `head.next` is always the most-recent real node; `tail.prev` is always the LRU.
- **Dict maps `key → Node`** (not `key → value`) — so you can find the node in O(1) and reposition it.

Operations:
- `get`: dict lookup → unhook node → re-insert at head.
- `put`: dict lookup + same unhook → create or update node → re-insert at head → check capacity and evict tail.prev if needed.

All O(1). Just verbose.

---

## 3. Comparison

| Aspect | OrderedDict version | Manual DLL version |
|---|---|---|
| Lines | ~15 | ~50 |
| Big-O | O(1) | O(1) |
| Uses stdlib | yes | no |
| Helper class needed | no | yes (Node) |
| Helper methods | no | yes (`_remove`, `_add_to_head`) |
| When to write | **first**, by default | only if asked to skip OrderedDict |

---

## 4. How to Practice

### Step 1: Read out loud (1 min)

> "LRU Cache needs O(1) get and put — that requires hash-map lookup PLUS the ability to reorder elements in constant time. Python's `OrderedDict` is exactly that combo: a dict that remembers insertion order with O(1) `move_to_end` and O(1) `popitem(last=False)`.
>
> On get: look up the key. If missing, return -1. If present, move it to the end (mark as most recent) and return the value.
> On put: if the key exists, move it to the end. Set the value. If size exceeds capacity, pop from the front (oldest) — that's the LRU eviction.
>
> All O(1). If asked to implement without OrderedDict, I'd build it manually with a hash map and a doubly-linked list with sentinel head and tail nodes."

### Step 2: Key Points

- **OrderedDict's `move_to_end(key)`** marks a key as most-recent in O(1).
- **`popitem(last=False)`** evicts the FRONT (oldest). Default is `last=True` (back).
- **On `put`, if the key exists, you MUST move it to end** — otherwise its position in the order is stale.
- **The capacity check goes AFTER the insert**, not before. Insert first, then check `len > capacity`.

### Step 3: Test Cases

| Sequence | Expected |
|---|---|
| capacity=2; put(1,1), put(2,2), get(1) | 1 |
| then put(3,3), get(2) | -1 (2 evicted) |
| then put(4,4), get(1) | -1 (1 evicted) |
| capacity=2; put(1,1), put(2,2), put(1,99) — update | get(2)=2, get(1)=99 (no eviction on update) |
| capacity=1; put(1,10), put(2,20) | get(1)=-1, get(2)=20 |

---

## 5. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting to `move_to_end` on `get` | Order stays stale; eviction picks the wrong key | Always move on access |
| Forgetting to `move_to_end` on `put` for existing key | Same issue — updated key shouldn't be LRU | Move first, then assign |
| `popitem(last=True)` instead of `last=False` | Evicts the MOST recent instead of the least recent | `last=False` for LRU |
| Building Node + DLL when OrderedDict would do | Wastes time, more code, more bugs | Lead with OrderedDict |

---

## 6. Interview Out-Loud Explanation

> "I need O(1) for both operations including the recency reordering, so I'll use `collections.OrderedDict` — it's a dict that remembers insertion order, with O(1) move-to-end and O(1) pop-from-front.
>
> `get(key)` looks up the key. If missing, return -1. If present, call `move_to_end(key)` to mark it as most recently used, then return the value.
>
> `put(key, value)` — if the key already exists, call `move_to_end` first. Then assign the value. After insertion, if `len(cache) > capacity`, call `popitem(last=False)` to evict the oldest entry.
>
> All O(1). If you want me to implement this without `OrderedDict`, I'd build a hash map mapping key to a doubly-linked-list node, with sentinel head and tail nodes to avoid empty-case branches."

That last sentence shows you know the harder version exists without forcing you to write it.

---

**Chain position:** LRU Cache is the canonical "design with O(1) ops" problem. The OrderedDict shortcut works here. For **Insert/Delete/GetRandom O(1)** the shortcut is different (dict + array with swap-and-pop). For **Find Median from Data Stream** it's two heaps. Each design medium has its own data structure combo.
