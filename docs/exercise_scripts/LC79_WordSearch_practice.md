# LC 79 — Word Search · Practice Script

---

## Problem

> Given an `m × n` grid of characters and a string `word`, return `True` if `word` can be constructed from letters of sequentially adjacent cells (4-directional). **A cell can be used at most once per word.**

**Constraints:**
- `1 <= m, n <= 6`
- `1 <= word.length <= 15`
- Letters are uppercase/lowercase English.

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Can the same cell be reused within one word?"** — No. This is THE constraint that forces the mark-and-unmark backtracking.
- **"Do diagonal moves count as adjacent?"** — No, 4-directional only. Decides the neighbor list.
- **"Am I allowed to mutate the board?"** — If yes, mark in place with `'#'`; if no, carry a visited set instead.
- **"Is matching case-sensitive?"** — Yes, `'A'` and `'a'` are different letters.
- **"Can the word be longer than the number of cells?"** — Constraints allow it (15 > 36 is false here, but ask) — if so, return False immediately.

---

## No meaningful brute force

Backtracking IS the natural approach for grid path-search. The "brute force" would be to enumerate every possible path of length L (4^L paths per starting cell) — which is exactly what backtracking does, just with pruning on mismatched characters cutting most subtrees. No meaningful slower baseline.

---

## RECOMMENDED — DFS + Backtracking (O(m·n·4^L))

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[i]:
                return False

            saved = board[r][c]
            board[r][c] = '#'          # mark used on this path

            found = (dfs(r+1, c, i+1) or dfs(r-1, c, i+1)
                  or dfs(r, c+1, i+1) or dfs(r, c-1, i+1))

            board[r][c] = saved        # backtrack
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False
```

### The pattern — DFS with backtracking

**DFS:** explore as deep as possible before backtracking.

**Backtracking** is the discipline: any state you change going IN, you must UNDO coming OUT. That way, sibling branches see a clean slate.

Here the state is the visited mark. We set `board[r][c] = '#'` on entry and restore the original char on exit. This guarantees the same cell can be reused in a DIFFERENT path attempt, but never twice in the same path.

### Why is this correct?

We try every possible starting cell. From each, we walk 4-directionally consuming one char of `word` at a time. If at any point the character doesn't match → dead end, backtrack. If we consume the entire `word` (`i == len(word)`) → success.

### Trace start on `board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]`, `word = "SEE"`

We scan for any `'S'` to start. First `'S'` is at (1,0).

- dfs(1,0,0): board[1][0]='S' matches word[0]='S'. Mark (1,0). Try neighbors for word[1]='E':
  - (2,0)='A' ✗
  - (0,0)='A' ✗
  - (1,1)='F' ✗
  - (1,-1) out of bounds
  - → backtrack, unmark (1,0)

Next `'S'` is at (1,3).
- dfs(1,3,0): matches 'S'. Mark. Neighbors for 'E':
  - (2,3)='E' ✓ → dfs(2,3,1): matches 'E'. Neighbors for word[2]='E':
    - (2,2)='E' ✓ → dfs(2,2,2): matches 'E'. i+1 == len(word) → **True** ✓

### Complexity

- **Time:** O(m · n · 4^L) where L = `len(word)`. Each starting cell launches a DFS that branches in up to 4 directions per step, for L steps.
- **Space:** O(L) recursion stack.

In practice it's much faster because of pruning (`board[r][c] != word[i]` cuts entire subtrees fast).

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting to restore the cell on backtrack | The cell stays `'#'` and is unusable by other paths → false negatives | Restore on exit |
| Using a `visited` set without backtracking it | Same problem — visited not cleared for next branch | Remove on exit |
| Restoring BEFORE `or`-chain finishes | Recursion sees corrupted state | Restore AFTER `found = ...` |
| Checking `i == len(word)` after the bounds check | If word has length 1, you skip the bounds correctly — be careful with order | Length check FIRST |
| Comparing char to `word` instead of `word[i]` | Always False (char vs str) | `word[i]` |

---

## Optimizations to mention

1. **Pruning by letter frequency:** if `Counter(word) - Counter(board cells) is non-empty`, return False immediately.
2. **Reverse the word** if its last letter is rarer than the first — fewer DFS starting points.
3. **Trie variant (Word Search II)** when matching many words at once.

---

## Interview Out-Loud

> "DFS with backtracking. From every cell, start a DFS that consumes word characters one at a time, walking 4-directionally. To prevent reusing a cell within the same path, I mark it on entry and restore on exit — that's the backtracking discipline.
>
> Base cases: consumed entire word → True. Out of bounds or mismatched char → False.
>
> Worst case O(m·n·4^L), but pruning on mismatch makes it much faster in practice. O(L) recursion stack."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect a twist after the base solution works.

- **"What if you can't modify the board?"** → Use a `visited` set: add `(r, c)` on entry, remove on exit. Same backtracking discipline, no mutation.
- **"Return the actual path, not just True/False."** → Carry a path list; append `(r, c)` going in, pop when backtracking. Return a copy on success.
- **"Now search for MANY words at once."** → That's Word Search II — a trie shares prefixes across words. One-line mention is enough; it's beyond medium scope.
- **"How would you make it faster in practice?"** → Letter-frequency prune up front, and reverse the word if its last letter is rarer than its first (fewer starting points).

---

**Chain position:** Backtracking on a grid. Same pattern in: Word Search II (with trie), Robot Room Cleaner, Sudoku Solver, N-Queens.
