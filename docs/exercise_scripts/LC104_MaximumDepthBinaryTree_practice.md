# LC 104 — Maximum Depth of Binary Tree · Practice Script

---

## Problem

> Given the root of a binary tree, return its **maximum depth** — the number of nodes along the longest path from root down to a leaf.

**Constraints:**
- Number of nodes: `0 <= n <= 10⁴`
- `-100 <= Node.val <= 100`

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
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

### The key idea

A tree's depth is **one of two things**:
1. **Empty tree** → 0
2. **Otherwise** → 1 + max depth of either subtree

That's literally it. Three lines.

This is the **simplest recursion pattern** you'll see — perfect for warming up on tree traversal. Each call asks the same question of a smaller problem: "what's the max depth below this node?"

### Trace on
```
        3
       / \
      9   20
         /  \
        15   7
```

| call | root | left depth | right depth | returns |
|---|---|---|---|---|
| maxDepth(3) | 3 | maxDepth(9) | maxDepth(20) | 1 + max(...) |
| maxDepth(9) | 9 | maxDepth(None)=0 | maxDepth(None)=0 | 1 + 0 = 1 |
| maxDepth(20) | 20 | maxDepth(15) | maxDepth(7) | 1 + max(...) |
| maxDepth(15) | 15 | 0 | 0 | 1 |
| maxDepth(7) | 7 | 0 | 0 | 1 |
| maxDepth(20) | — | 1 | 1 | 2 |
| maxDepth(3) | — | 1 | 2 | **3** ✓ |

### Complexity

- **Time:** O(n) — visit every node once
- **Space:** O(h) — recursion stack, where `h` is tree height. Worst case (skewed tree) → O(n). Balanced tree → O(log n).

---

## ALTERNATIVE — Iterative BFS (O(n))

```python
from collections import deque

class Solution:
    def maxDepth(self, root):
        if not root:
            return 0
        queue = deque([root])
        depth = 0
        while queue:
            depth += 1
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)
        return depth
```

Level-by-level scan. Useful when you want to AVOID recursion stack (very deep trees). Same big-O.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Returning 0 for a single-node tree | Off-by-one — a leaf has depth 1, not 0 | Empty tree → 0; otherwise add the `1 +` |
| Using `min` instead of `max` | Returns min depth (different problem!) | `max` |
| Forgetting the base case | Infinite recursion / NPE | `if not root: return 0` FIRST |

---

## Interview Out-Loud

> "Recursion. Base case: empty tree → 0. Otherwise, the depth of this tree is 1 plus the max depth of the deeper of the two subtrees.
>
> Three lines. O(n) time — every node visited once. O(h) recursion stack space — h is the tree height. Balanced tree → O(log n) stack. Skewed tree → O(n) stack."

---

**Chain position:** Foundational tree recursion. Same recursion shape in: Invert Binary Tree, Diameter, Balanced Binary Tree, Same Tree.
