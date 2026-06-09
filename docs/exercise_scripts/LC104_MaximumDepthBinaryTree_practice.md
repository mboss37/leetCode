# LC 104 — Maximum Depth of Binary Tree · Practice Script

---

## Problem

> Given the root of a binary tree, return its **maximum depth** — the number of nodes along the longest path from root down to a leaf.

**Constraints:**
- Number of nodes: `0 <= n <= 10⁴`
- `-100 <= Node.val <= 100`

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on pinning down requirements first — pick the ones that genuinely change your code:

- **"Is depth counted in nodes or edges?"** — Nodes here: a single node has depth 1. This is the classic off-by-one; settle it before coding.
- **"Can the tree be empty?"** — Yes. Return 0 — that is the base case.
- **"How deep can the tree be? Is recursion safe?"** — Up to 10⁴ nodes, possibly fully skewed. Mention iterative BFS if stack depth worries them.
- **"Maximum depth, not minimum?"** — Maximum. Minimum depth is a different problem with a leaf subtlety — do not mix them up.

---

## No meaningful brute force

You must visit every node to know the depth — that's the O(n) floor. The recursion below IS the simplest expression of that visit-every-node pass; no slower baseline worth showing.

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

## Likely Follow-ups

One question, several parts — this warmup almost always grows.

- **"Do it without recursion."** → The Iterative BFS alternative above: depth = number of levels drained.
- **"Now minimum depth."** → Careful: must reach a LEAF. A node with one child cannot take `min` with the missing side's 0 — handle the one-child case.
- **"Now the diameter, or check if it's balanced."** → Same recursion shape; combine the two subtree depths differently (sum for diameter, |diff| ≤ 1 for balanced).
- **"Return the values level by level."** → That is Level Order Traversal — see the LC 102 practice script in this repo.

---

**Chain position:** Foundational tree recursion. Same recursion shape in: Invert Binary Tree, Diameter, Balanced Binary Tree, Same Tree.
