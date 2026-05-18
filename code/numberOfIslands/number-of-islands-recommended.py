# Practice script: docs/exercise_scripts/LC200_NumberOfIslands_practice.md

from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # Walk the grid. Every time we hit a '1' we haven't seen, that's a
        # new island — flood-fill its entire connected component to '0' so
        # we don't count it again.
        #
        # DFS via recursion is the cleanest expression here.

        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        count = 0

        def dfs(r: int, c: int) -> None:
            # Out of bounds or already water? stop.
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
                return
            grid[r][c] = "0"   # mark visited (sink the land)
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    count += 1
                    dfs(r, c)

        return count


# ============= TEST CASES =============
solution = Solution()

g1 = [
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"],
]
print(solution.numIslands(g1))   # 1

g2 = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"],
]
print(solution.numIslands(g2))   # 3

g3 = [["0"]]
print(solution.numIslands(g3))   # 0

g4 = [["1"]]
print(solution.numIslands(g4))   # 1
