# LC 200 — Number of Islands · Practice Script

---

## Problem

> Given an `m × n` grid of `'1'` (land) and `'0'` (water), count the number of **islands**. An island is a 4-directionally connected group of land cells. The grid is bordered by water on all sides.

**Constraints:**
- `1 <= m, n <= 300`
- Cells are `'1'` or `'0'` (strings, not ints).

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Do diagonal neighbors count as connected?"** — No, 4-directional only. With diagonals I'd just add 4 more directions.
- **"Am I allowed to mutate the grid?"** — If yes, sink `'1'` to `'0'` as my visited mark; if no, I need a visited set.
- **"Are cells strings or ints?"** — Strings. Comparing to int `1` silently matches nothing and returns 0.
- **"How big can the grid get?"** — 300×300. A snaking island could mean ~90k deep recursion — worth offering the BFS variant.

---

## The pattern — connected-component count via flood fill

For every cell:
- If it's water or already visited → skip.
- Else → it's the START of a new island. **Increment counter.** Then **flood-fill** the whole connected component so we don't count it again.

Flood fill = DFS or BFS from this cell, visiting all 4-neighbors that are land, marking them visited.

---

## No meaningful brute force

Connected-components on a grid — DFS or BFS IS the standard tool. The Union-Find alternative is asymptotically the same. There's no "slower but simpler" baseline to contrast: you either traverse the grid once or you don't.

---

## RECOMMENDED — DFS, sink-as-you-go (O(m·n))

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0
        rows, cols = len(grid), len(grid[0])
        count = 0

        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != '1':
                return
            grid[r][c] = '0'           # sink the land
            dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1
                    dfs(r, c)
        return count
```

### Why DFS works

DFS from a `'1'` cell visits **every cell in its connected island** before returning. By sinking each visited cell to `'0'`, the outer loop's later iterations never re-enter the same island.

### "Mark visited" without extra space

We mutate the grid: `'1' → '0'`. Saves O(m·n) `visited` set space.

If the grid must stay unchanged → use a `visited: set[(r, c)]` instead. Time/space both O(m·n).

### Trace on
```
1 1 0
1 0 0
0 0 1
```

| (r,c) | val | action |
|---|---|---|
| (0,0) | 1 | new island #1, dfs sinks (0,0), (0,1), (1,0) |
| (0,1) | 0 (sunk) | skip |
| (0,2) | 0 | skip |
| (1,0) | 0 (sunk) | skip |
| (1,1) | 0 | skip |
| (1,2) | 0 | skip |
| (2,0) | 0 | skip |
| (2,1) | 0 | skip |
| (2,2) | 1 | new island #2, dfs sinks (2,2) |

Count: **2** ✓

### Complexity

- **Time:** O(m·n) — every cell visited at most once
- **Space:** O(m·n) worst case for recursion stack (one giant island shaped like a spiral)

---

## ALTERNATIVE — BFS (avoid deep recursion)

```python
from collections import deque

class Solution:
    def numIslands(self, grid):
        if not grid or not grid[0]:
            return 0
        rows, cols = len(grid), len(grid[0])
        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1
                    q = deque([(r, c)])
                    grid[r][c] = '0'
                    while q:
                        x, y = q.popleft()
                        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                            nx, ny = x+dx, y+dy
                            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                                grid[nx][ny] = '0'
                                q.append((nx, ny))
        return count
```

Use BFS if interviewer is worried about stack overflow on huge grids. Same big-O.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Comparing `grid[r][c] == 1` (int) | Grid is strings — comparison always False, count = 0 | `'1'` not `1` |
| Missing the bounds check | Index out of range when walking off the grid | First line of DFS |
| Forgetting to mark visited | Infinite recursion or double-counting | Sink on entry |
| Marking visited AFTER recursing | Re-enter from neighbors → infinite | Mark BEFORE the 4 recursive calls |
| Counting every `'1'` cell instead of islands | Returns total land cells, not islands | Increment only when STARTING a new flood fill |

---

## Interview Out-Loud

> "Connected components on a grid. Walk every cell. When I see land that hasn't been visited, it's a new island — increment the counter and flood-fill its entire component to mark it visited, so the outer loop doesn't re-enter.
>
> I'll use DFS and mutate the grid in-place ('1' to '0') as my visited marker — saves the visited-set space. If the grid must stay unchanged, swap in a set.
>
> Every cell visited at most once → O(m·n) time. Worst case O(m·n) recursion stack for a snaking island. BFS variant avoids that."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect a twist after the base solution works.

- **"Now return the size of the LARGEST island."** → Max Area of Island: make `dfs` return the number of cells it sank, track the max instead of counting starts.
- **"You can't modify the grid."** → Swap the sinking for a `visited` set of `(r, c)` tuples. Same traversal, O(m·n) extra space.
- **"Return the perimeter of an island."** → For each land cell, add 1 for every neighbor that is water or out of bounds.
- **"What if islands connect diagonally too?"** → Extend the direction list to 8 neighbors; everything else stays the same.

---

**Chain position:** Grid traversal / connected components. Same pattern in: Max Area of Island, Surrounded Regions, Pacific Atlantic, Walls and Gates.
