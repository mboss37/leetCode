# Practice script: docs/exercise_scripts/LC102_BinaryTreeLevelOrder_practice.md

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: "Optional[TreeNode]" = None,
        right: "Optional[TreeNode]" = None,
    ):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # BFS, processing the queue one LEVEL at a time.
        # Trick: at the start of each iteration, len(queue) == nodes on this level.
        # Drain exactly that many before moving to the next level.

        if not root:
            return []

        result: List[List[int]] = []
        queue: deque = deque([root])

        while queue:
            level: List[int] = []
            for _ in range(len(queue)):       # snapshot this level's size
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)

        return result


# ============= TEST HELPERS =============
def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    q = [root]
    i = 1
    while q and i < len(values):
        node = q.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


# ============= TEST CASES =============
solution = Solution()

print(solution.levelOrder(build([3, 9, 20, None, None, 15, 7])))  # [[3],[9,20],[15,7]]
print(solution.levelOrder(build([1])))                              # [[1]]
print(solution.levelOrder(build([])))                                # []
print(solution.levelOrder(build([1, 2, 3, 4, 5, 6, 7])))            # [[1],[2,3],[4,5,6,7]]
