# LC 206 — Reverse Linked List · Practice Script

---

## Problem

> Given the head of a singly linked list, reverse the list and return the new head.

**Constraints:**
- Number of nodes: `0 <= n <= 5000`
- `-5000 <= Node.val <= 5000`

---

## No meaningful brute force

Linked-list traversal is inherently O(n) — you must touch every node. The pointer-juggling approach below is the simplest correct version; there's no slower comparative worth writing as a baseline. (A recursive variant exists but trades stack for clarity, not complexity.)

---

## RECOMMENDED — Iterative, Three Pointers (O(n))

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            next_node = curr.next   # save the rest of the list
            curr.next = prev        # flip current's arrow backwards
            prev = curr             # prev moves up
            curr = next_node        # curr moves up
        return prev
```

### The key idea

Walk the list once. At every node, **flip its `.next` arrow to point backwards** instead of forwards.

The trick: before you overwrite `curr.next`, you must SAVE the original next, or you lose the rest of the list.

Three pointers:
- **`prev`** — the last node we already reversed. Starts as `None` (the new tail).
- **`curr`** — the node we're flipping right now.
- **`next_node`** — temporary save of `curr.next` so we don't lose the chain.

### Trace on `1 → 2 → 3 → None`

```
Start:   prev = None,  curr = 1
```

| iter | curr (start) | `next_node = curr.next` | `curr.next = prev` | `prev = curr` | `curr = next_node` |
|---|---|---|---|---|---|
| 1 | 1 | next_node = 2 | 1.next → None | prev = 1 | curr = 2 |
| 2 | 2 | next_node = 3 | 2.next → 1 | prev = 2 | curr = 3 |
| 3 | 3 | next_node = None | 3.next → 2 | prev = 3 | curr = None |

Loop exits (curr is None). `return prev = 3`. New chain: `3 → 2 → 1 → None` ✓

### Complexity

- **Time:** O(n) — visit each node once
- **Space:** O(1) — three pointers, no extra structures

---

## ALTERNATIVE — Recursive (O(n) time, O(n) stack space)

```python
class Solution:
    def reverseList(self, head):
        if not head or not head.next:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head    # make next node point back to me
        head.next = None         # cut my forward link
        return new_head
```

Why O(n) space? The recursion stack goes `n` levels deep before unwinding.

**Interview tip:** prefer the iterative version. Recursive is elegant but eats stack space. Both are O(n) time — iterative is O(1) space.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting to save `curr.next` before overwriting | Lose the rest of the list — infinite loop or NPE | Save `next_node = curr.next` FIRST |
| Returning `head` instead of `prev` | Returns the OLD head (now the tail) — wrong | Return `prev` (the new head) |
| Starting `prev = head` instead of `None` | New tail still points to old head → cycle | `prev = None` so the original head becomes the new tail with `.next = None` |
| Forgetting the `while curr` check on empty list | NPE on `head = None` | Loop guard handles it; returns `None` correctly |

---

## Interview Out-Loud

> "Three pointers: prev, curr, next_node. Walk the list once. At every step: save curr's next, flip curr's arrow to point at prev, then advance both prev and curr forward.
>
> The key is saving the next pointer BEFORE overwriting it — otherwise we lose the rest of the list.
>
> When curr is None, prev is the new head. O(n) time, O(1) space."

---

**Chain position:** Foundational linked-list manipulation. Same pointer-juggling pattern in: Remove Nth Node, Reorder List, Reverse Sublist, Palindrome Linked List.
