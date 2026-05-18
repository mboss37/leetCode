# Practice script: docs/exercise_scripts/LC79_WordSearch_practice.md

from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        # Try DFS from every cell. From each cell, walk 4-directionally,
        # consuming one character of `word` at each step.
        #
        # To avoid revisiting a cell within the SAME path, we mark it
        # temporarily ('#') on the way in and restore it on the way out.
        # This is "backtracking" — we always restore state when leaving.

        rows, cols = len(board), len(board[0])

        def dfs(r: int, c: int, i: int) -> bool:
            if i == len(word):
                return True   # consumed all chars
            if r < 0 or c < 0 or r >= rows or c >= cols:
                return False
            if board[r][c] != word[i]:
                return False

            saved = board[r][c]
            board[r][c] = "#"   # mark visited on THIS path

            found = (
                dfs(r + 1, c, i + 1)
                or dfs(r - 1, c, i + 1)
                or dfs(r, c + 1, i + 1)
                or dfs(r, c - 1, i + 1)
            )

            board[r][c] = saved   # backtrack — restore the cell
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False


# ============= TEST CASES =============
solution = Solution()

board = [
    ["A", "B", "C", "E"],
    ["S", "F", "C", "S"],
    ["A", "D", "E", "E"],
]

print(solution.exist(board, "ABCCED"))   # True
print(solution.exist(board, "SEE"))      # True
print(solution.exist(board, "ABCB"))     # False (would need to reuse 'B')
print(solution.exist(board, "A"))        # True
print(solution.exist(board, "XYZ"))      # False
