# LC 380 — Insert / Delete / GetRandom in O(1) · Practice Script

---

## Problem

> Implement `RandomizedSet`:
> - `insert(val)` → adds val. Returns `True` if it wasn't there, else `False`.
> - `remove(val)` → removes val. Returns `True` if it was there, else `False`.
> - `getRandom()` → returns a uniformly random element from the set.
>
> **All three operations must be O(1) average.**

**Constraints:**
- Values in `[-2³¹, 2³¹-1]`
- Up to 2×10⁵ calls
- `getRandom` only called when the set has elements

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Are duplicates allowed, or is this a true set?"** — True set here. `insert` of an existing value returns False. Duplicates is the LC 381 follow-up.
- **"Must getRandom be uniform over the CURRENT elements?"** — Yes. That's the whole reason a dict alone fails — you need a list to sample from.
- **"Is O(1) average acceptable, or strict worst case?"** — Average. Dict operations are average O(1), and that's what the spec means.
- **"Can getRandom be called on an empty set?"** — No, guaranteed non-empty — no empty-check needed.
- **"What do insert/remove return?"** — Booleans: True if the state actually changed.

---

## The trick — pair a list with a dict

| Structure | Provides | Doesn't provide |
|---|---|---|
| **list** | O(1) random access by index, O(1) random sampling | O(n) lookup, O(n) middle-removal |
| **dict (set)** | O(1) lookup, O(1) insert/delete | NO random sampling |

Either alone fails. **Both together** give us everything in O(1):

- **list `items`** — the values, in arbitrary positions
- **dict `idx`** — `{value → index in items}`

`getRandom` needs the list (random.choice). Lookup needs the dict. The clever part is REMOVAL.

---

## No meaningful brute force

Design problem — the O(1) per-operation requirement IS the constraint. The "naive" alternative (e.g., a list alone, scanning on every remove) is O(n) per remove, which **violates the spec**, not a comparative baseline. The pair-of-structures design below is the minimal correct answer.

---

## RECOMMENDED — List + Dict, swap-with-last trick (O(1))

```python
import random

class RandomizedSet:
    def __init__(self):
        self.items = []
        self.idx = {}

    def insert(self, val: int) -> bool:
        if val in self.idx:
            return False
        self.idx[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.idx:
            return False
        i = self.idx[val]
        last_val = self.items[-1]
        self.items[i] = last_val      # overwrite target with last
        self.idx[last_val] = i        # update last's new position
        self.items.pop()              # O(1) pop from end
        del self.idx[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.items)
```

### Why the swap-with-last trick

To delete from the middle of a list in O(1), you can't shift everything down — that's O(n). So:

1. **Look up** the target's index `i` via the dict.
2. **Overwrite** position `i` with the LAST element (so target is gone).
3. **Update the dict** so the moved-element's new index = `i`.
4. **Pop** the last element (now a duplicate). `list.pop()` from the end is O(1).
5. **Delete** the target from the dict.

Order is intact? No — the list is now in a weird order. But we don't care: we only ever query by random index, never by position.

### Trace on `insert(1), insert(2), insert(3), remove(2)`

After all inserts:
- `items = [1, 2, 3]`
- `idx = {1: 0, 2: 1, 3: 2}`

`remove(2)`:
- `i = idx[2] = 1`
- `last_val = items[-1] = 3`
- `items[1] = 3` → `items = [1, 3, 3]`
- `idx[3] = 1`
- `items.pop()` → `items = [1, 3]`
- `del idx[2]` → `idx = {1: 0, 3: 1}`

State after: `items = [1, 3]`, `idx = {1: 0, 3: 1}` ✓

### Complexity

- **All three operations:** O(1) average
- **Space:** O(n)

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting to update `idx[last_val]` | Dict points to the wrong (popped) position → corrupt state | Update `idx[last_val] = i` BEFORE pop |
| Popping `items[i]` directly | O(n) shift | Swap-then-pop-end |
| Special-casing "i is already last" | Unnecessary — the code works the same way | Same code path; `items[-1] = items[-1]` is a no-op |
| Using `set` instead of dict | `set` has no "give me the i-th element" operation | Need dict with INDICES |
| Using `random.randint` on a stale length | Off-by-one if you forget to use current `len` | `random.choice(self.items)` (cleanest) |

---

## Interview Out-Loud

> "I need O(1) on all three. A list gives me O(1) random access and random sampling but O(n) for middle-removal. A dict gives me O(1) lookup but no random sampling. So I'll pair them.
>
> The list holds the values. The dict maps value → its index in the list.
>
> Insert: append to list, record the new index in the dict.
>
> Remove is the trick: to delete from the list in O(1), I swap the target with the LAST element, then pop the last. I also update the dict for the swapped element's new index, and delete the target's entry.
>
> getRandom: random.choice on the list.
>
> All O(1) average. O(n) space."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect one of these next:

- **"Now allow DUPLICATES."** → LC 381. The dict maps value → SET of indices. On remove, swap one index with the last element and update the moved value's index set.
- **"Make getRandom weighted — value with weight w is w times more likely."** → Store cumulative weights, pick a random number, binary search for its slot (LC 528 idea).
- **"Why only AVERAGE O(1)?"** → Dict ops can degrade on hash collisions, and list append occasionally reallocates. Amortized/average is what holds; ballpark is enough.
- **"What if remove targets the last element?"** → Same code path — it overwrites itself, then pops. Walk that trace to show no special case is needed.

---

**Chain position:** Compound data-structure design. Pairing structures to get the best of both is a recurring trick — same flavor as LRU Cache (hash + DLL or `OrderedDict`).
