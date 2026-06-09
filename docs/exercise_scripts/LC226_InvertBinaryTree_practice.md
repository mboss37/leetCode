# LC 226 — Invert Binary Tree · Practice Script

---

## Problem

> Given the root of a binary tree, invert it (mirror it left-to-right) and return the root.

**Constraints:**
- Number of nodes: `0 <= n <= 100`
- `-100 <= Node.val <= 100`

**Background:** The infamous "Max Howell / Homebrew" interview question.

---

## Clarifying Questions (ask 2-3 before you code)

Requirements come before code — pick the ones that genuinely change your approach:

- **"Mutate the tree in place, or return a new copy?"** — In place is expected; you return the same root. A copy doubles the work for nothing.
- **"What exactly does invert mean?"** — Mirror left-to-right: swap the two children at EVERY node, all the way down.
- **"Can the tree be empty?"** — Yes. Return None — that is the base case.
- **"How big can it get? Recursion OK?"** — At most 100 nodes here, so stack depth is a non-issue. Say so, then offer BFS anyway.

---

## No meaningful brute force

Inverting the tree requires touching every node to swap its children — O(n) is the floor. The recursion below is the simplest correct version; no slower comparative exists.

---

## RECOMMENDED — Recursion (O(n))

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
```

### The key idea

At every node:
1. **Swap** its left and right children.
2. **Recurse** into both subtrees (which then do the same).

That's it. The Python tuple-swap `a, b = b, a` does it in one line — and because it evaluates the RHS first, the recursion happens before the assignment.

### Trace on
```
       4                  4
      / \                / \
     2   7    →         7   2
    /\   /\            /\   /\
   1  3 6  9          9  6 3  1
```

Recursion unwinds bottom-up: leaves swap (trivially, since they have no children), then each parent swaps its (now-inverted) subtrees.

### Complexity

- **Time:** O(n) — visit every node once
- **Space:** O(h) — recursion stack, h = tree height. Balanced → O(log n). Skewed → O(n).

---

## ALTERNATIVE — Iterative BFS (O(n))

```python
from collections import deque

class Solution:
    def invertTree(self, root):
        if not root:
            return None
        queue = deque([root])
        while queue:
            node = queue.popleft()
            node.left, node.right = node.right, node.left
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        return root
```

BFS through the tree, swap at every node. Same big-O.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting base case | NPE on None root | `if not root: return None` FIRST |
| Recursing then swapping (wrong order without tuple) | The recursion sees the ALREADY-SWAPPED children and inverts twice | Use tuple swap OR save one in a temp var |
| Calling `invertTree(root.left)` and assigning to `root.left` directly | If you do this for left first then right, you've changed what `root.right` should be inverted from — easy bug | Use the one-line tuple swap |

---

## Interview Out-Loud

> "Recursion. At every node: swap left and right children, then recurse into both. Base case is an empty subtree — return None.
>
> Python tuple swap evaluates the right side first, so the recursion happens before the assignment — clean one-liner.
>
> O(n) time — every node visited once. O(h) recursion stack. Balanced tree → log n stack."

---

## Likely Follow-ups

One question that grows in parts — the swap is rarely where it ends.

- **"Do it iteratively."** → The BFS alternative above: dequeue a node, swap its children, enqueue both. A stack (DFS) works the same way.
- **"Why does the one-line tuple swap not double-invert?"** → Python evaluates the right side first, so both recursions run on the ORIGINAL children before assignment.
- **"Check if a tree is a mirror of itself."** → Symmetric Tree: compare left and right subtrees pairwise — outer with outer, inner with inner.
- **"Same recursion shape, different combine?"** → Maximum Depth — see the LC 104 practice script in this repo.

---

**Chain position:** Foundational tree recursion (same shape as Max Depth). Related: Symmetric Tree, Same Tree.
