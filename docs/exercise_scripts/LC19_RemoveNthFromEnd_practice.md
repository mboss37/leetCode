# LC 19 — Remove Nth Node From End of List · Practice Script

**Code:** [code/removeNthFromEnd/](../../code/removeNthFromEnd/)

---

## Problem

> Given the head of a linked list, remove the `n`-th node from the END of the list and return its head.

**Constraints:**
- `1 <= n <= length of list <= 30`
- Values in range `[0, 100]`

**Follow-up:** Solve in one pass.

---

## RECOMMENDED — Two Pointers with Gap, One Pass (O(n))

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        slow = fast = dummy

        # Move fast n steps ahead — creates a gap of n between slow and fast.
        for _ in range(n):
            fast = fast.next

        # Walk both pointers together until fast hits the last node.
        while fast.next:
            slow = slow.next
            fast = fast.next

        # slow is now right before the node to remove. Skip it.
        slow.next = slow.next.next
        return dummy.next
```

### The key idea — gap pointers

Keep `slow` and `fast` exactly `n` apart. When `fast` reaches the **last node**, `slow` is sitting at the node **right before** the one we want to remove.

Then: `slow.next = slow.next.next` skips the target node.

### Why the dummy node?

If we're removing the actual HEAD (e.g. `n` equals list length), we need a node BEFORE the head to be our `slow` pointer. The dummy gives us that. Return `dummy.next` at the end — the new head.

Without dummy: ugly special case for "remove head."

### Trace on `[1, 2, 3, 4, 5], n = 2`

Dummy → 1 → 2 → 3 → 4 → 5

| step | slow at | fast at | note |
|---|---|---|---|
| init | dummy | dummy | both at dummy |
| advance fast n=2 steps | dummy | 2 | gap = 2 |
| iter 1 | 1 | 3 | |
| iter 2 | 2 | 4 | |
| iter 3 | 3 | 5 | fast.next = None → exit |
| skip | — | — | slow.next (=4) skipped: 3.next = 5 |

Result: `[1, 2, 3, 5]` ✓ (the 2nd-from-end was 4)

### Complexity

- **Time:** O(n) — single pass
- **Space:** O(1)

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| No dummy node when removing head | Special-case the head separately (ugly) | Always use dummy → simpler |
| Advancing fast `n+1` times | Off-by-one; slow ends up at the target, not before it | Exactly `n` advances |
| Using `while fast` instead of `while fast.next` | slow walks one step too far | Stop when fast is at the LAST node, not after |
| Returning `head` instead of `dummy.next` | Wrong when head was the removed node | Always `dummy.next` |

---

## Interview Out-Loud

> "Two-pointer gap trick. Put a dummy before head — handles the edge case of removing the head itself. Both pointers start at dummy.
>
> Move fast n steps ahead. Now there's a gap of n between them. Walk both together until fast hits the last node (fast.next is None). At that point slow sits right BEFORE the node to remove.
>
> Skip the target: slow.next = slow.next.next. Return dummy.next.
>
> O(n) time, O(1) space. One pass."

---

**Chain position:** Two-pointer linked-list trick. Same gap pattern in: Middle of Linked List, Linked List Cycle.
