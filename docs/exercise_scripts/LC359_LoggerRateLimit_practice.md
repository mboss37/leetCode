# LC 359 — Logger Rate Limiter · Practice Script

---

## Problem

> Design a logger that decides whether each `message` should be printed at the given `timestamp`. A message can be printed if it has NOT been printed in the **last 10 seconds**.
>
> Implement `shouldPrintMessage(timestamp, message) -> bool`.

**Constraints:**
- Timestamps are non-negative and arrive in **non-decreasing** order.
- Up to 10⁴ calls.

---

## RECOMMENDED — Dict of last-seen timestamps (O(1) per call)

```python
class Logger:
    def __init__(self):
        self.last_seen = {}    # message -> last timestamp it was printed

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        prev = self.last_seen.get(message)
        if prev is not None and timestamp - prev < 10:
            return False
        self.last_seen[message] = timestamp
        return True
```

### The key idea

Don't store ALL timestamps for each message. Just the **most recent one** that was actually printed.

When the same message comes in again:
- If `now - last_seen[message] < 10` → suppress, **don't update**.
- Else → print, update `last_seen[message] = now`.

Crucial detail: when suppressing, **do NOT update the timestamp**. Suppressed messages don't reset the cooldown clock — the cooldown is measured from the LAST PRINTED time.

### Trace

| timestamp | message | last_seen[message] | diff | action |
|---|---|---|---|---|
| 1 | "foo" | — (new) | — | print, last_seen["foo"] = 1 |
| 2 | "bar" | — | — | print, last_seen["bar"] = 2 |
| 3 | "foo" | 1 | 2 < 10 | suppress, last_seen unchanged |
| 8 | "bar" | 2 | 6 < 10 | suppress |
| 10 | "foo" | 1 | 9 < 10 | suppress |
| 11 | "foo" | 1 | 10 NOT < 10 | print, last_seen["foo"] = 11 |

### Complexity

- **Time:** O(1) per call
- **Space:** O(M) where M = number of distinct messages ever seen

---

## Edge cases

| Case | Handled because |
|---|---|
| First time seeing a message | `prev is None` → print |
| Same timestamp, same message | `0 < 10` → suppress (correct: still within window) |
| Exactly 10 seconds later | `10 < 10` is False → print (boundary is inclusive at exactly 10) |
| Different messages at same time | Independent entries in the dict — no interaction |

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Updating timestamp on suppressed messages | Cooldown never expires for chatty messages | Only update when printing |
| Using `<=` instead of `<` | Off-by-one: exactly 10s gap should be allowed | Strict `<` |
| Building a queue of all timestamps | Wastes memory; not needed | Just the last one |
| Forgetting `prev is not None` check | KeyError on first-time messages | `.get()` returns None safely |

---

## Memory cleanup follow-up

> **Interviewer:** "Memory grows forever. Fix it."

Two clean fixes:

**1. Queue of (timestamp, message) pairs, pop ones older than now-10:**

```python
from collections import deque

class Logger:
    def __init__(self):
        self.queue = deque()
        self.recent = set()

    def shouldPrintMessage(self, timestamp, message):
        # Drop expired entries.
        while self.queue and self.queue[0][0] <= timestamp - 10:
            t, m = self.queue.popleft()
            self.recent.discard(m)
        if message in self.recent:
            return False
        self.queue.append((timestamp, message))
        self.recent.add(message)
        return True
```

Memory bounded by the 10s window. Same O(1) amortized.

**2. Periodic sweep** every N calls — simpler but spiky.

---

## Interview Out-Loud

> "Dict from message to its last PRINTED timestamp. On each call: if the message was printed within the last 10 seconds, suppress and don't touch the dict. Otherwise print and update.
>
> Strict less-than on the gap — exactly 10 seconds is allowed.
>
> O(1) per call. Memory grows with unique messages. Bounded variant: pair a deque with a set, evict entries older than timestamp - 10 on each call."

---

**Chain position:** Hash-based rate limiting. Same idea scaled up in: Hit Counter, Throttling Requests Per Second.
