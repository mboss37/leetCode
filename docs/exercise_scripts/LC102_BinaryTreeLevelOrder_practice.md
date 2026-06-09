# LC 102 — Binary Tree Level Order Traversal · Practice Script

---

## Problem

> Given the root of a binary tree, return the values **level by level**, top to bottom, left to right.

**Example:**
```
        3
       / \
      9   20
         /  \
        15   7
```
Returns `[[3], [9, 20], [15, 7]]`.

**Constraints:**
- Number of nodes: `0 <= n <= 2000`
- `-1000 <= Node.val <= 1000`

---

## Clarifying Questions (ask 2-3 before you code)

Requirements capture is scored before any code goes down — pick the ones that genuinely shape your approach:

- **"Can the tree be empty?"** — Yes, 0 nodes. Return `[]` — that is the early return at the top.
- **"One flat list, or a list per level?"** — A list per level. This is exactly why plain BFS is not enough and you need the level-size snapshot.
- **"Left-to-right within each level?"** — Yes. Enqueue the left child before the right.
- **"Any shape guarantee — balanced, complete?"** — No. The queue can hold about half the nodes at the widest level; worth saying for space.
- **"Values can repeat or be negative?"** — Yes to both; the traversal never looks at values, so nothing changes.

---

## The pattern — BFS with level-size snapshot

Plain BFS visits nodes in level order but doesn't TELL you when a level ends. The trick:

**At the start of every iteration of the outer loop, `len(queue)` equals the number of nodes on the current level.** Process exactly that many. Anything added to the queue during that batch belongs to the NEXT level.

---

## No meaningful brute force

Level-order traversal must visit every node — O(n) is the floor. BFS with a queue is the canonical expression of that visit. No slower comparative worth writing.

---

## RECOMMENDED — BFS, level-by-level (O(n))

```python
from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        result, queue = [], deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):     # snapshot the level's size
                node = queue.popleft()
                level.append(node.val)
                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)
            result.append(level)
        return result
```

### Why `len(queue)` at the START of the loop

Inside the inner `for`, we pop nodes from the front AND append their children to the back. If we called `len(queue)` on every iteration, it would mix current-level removals with next-level additions and we'd never finish the level cleanly.

By snapshotting `len(queue)` BEFORE the inner loop, we lock in the boundary: "drain exactly this many. After that, everything in the queue is the next level."

### Trace on the example tree

| iter | queue before | level size | pop in order | level added | queue after |
|---|---|---|---|---|---|
| 1 | [3] | 1 | 3 | [3] | [9, 20] |
| 2 | [9, 20] | 2 | 9, 20 | [9, 20] | [15, 7] |
| 3 | [15, 7] | 2 | 15, 7 | [15, 7] | [] |
| exit | | | | | result = [[3],[9,20],[15,7]] ✓ |

### Why `deque` (not list)

`deque.popleft()` is **O(1)**. `list.pop(0)` is **O(n)** — it shifts everything. With n up to thousands, that's a real difference.

### Complexity

- **Time:** O(n) — each node enqueued and dequeued once
- **Space:** O(n) — output + queue (worst case is the bottom level, ~n/2 nodes)

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Using `list` and `pop(0)` | Each pop is O(n) → total O(n²) | `collections.deque` |
| Recomputing `len(queue)` inside the loop | Inner loop sees next-level adds → never finishes correctly | Snapshot it ONCE before the `for` |
| Pushing None children | NoneType has no `.val` | Guard with `if node.left:` and `if node.right:` |
| Returning `[]` for None root only if you forget the early return | Crash on `deque([None])` | Early return at the top |

---

## Variants and follow-ups

| Variant | Tweak |
|---|---|
| **Zigzag / Spiral order (LC 103)** | Append `level` reversed on odd levels |
| **Bottom-up Level Order (LC 107)** | Return `result[::-1]` |
| **Right Side View (LC 199)** | Append only the LAST node of each level |
| **Average of Levels (LC 637)** | Compute mean of each `level` |

All are the same skeleton with a 1-line tweak.

---

## Interview Out-Loud

> "BFS with a queue, processing one level at a time. The key trick: at the start of each outer iteration, len(queue) equals the number of nodes on the current level — I snapshot it, drain exactly that many, and everything left after is the next level.
>
> Use `collections.deque` so popleft is O(1). Each node is enqueued once and dequeued once → O(n) time. O(n) space for the queue.
>
> Same skeleton extends to zigzag, right-side-view, average-of-levels — change just the append step."

---

## Likely Follow-ups

One question that grows in parts — every extension here is the same skeleton with a one-line change.

- **"Now zigzag: alternate left-to-right and right-to-left per level."** → Keep a level counter; reverse `level` before appending on odd levels (LC 103).
- **"Return levels bottom-up."** → Same loop, return `result[::-1]` at the end (LC 107).
- **"Return what you'd see from the right side."** → Append only the last node of each level (LC 199).
- **"Just the depth of the tree?"** → Count outer-loop iterations — that is Maximum Depth, see the LC 104 practice script in this repo.

---

**Chain position:** Foundational tree BFS. Skeleton for: Zigzag Level Order, Right Side View, Average of Levels, Bottom-Up Level Order.
