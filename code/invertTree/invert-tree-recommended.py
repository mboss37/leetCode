# Practice script: docs/exercise_scripts/LC226_InvertBinaryTree_practice.md

from typing import Optional


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
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # At every node: swap its children, then recurse into both.
        # Python's tuple swap does it in one line.

        if not root:
            return None

        root.left, root.right = (
            self.invertTree(root.right),
            self.invertTree(root.left),
        )
        return root


# ============= TEST HELPERS =============
def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def level_order(root):
    if not root:
        return []
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


# ============= TEST CASES =============
solution = Solution()

print(level_order(solution.invertTree(build([4, 2, 7, 1, 3, 6, 9]))))   # [4, 7, 2, 9, 6, 3, 1]
print(level_order(solution.invertTree(build([2, 1, 3]))))                # [2, 3, 1]
print(level_order(solution.invertTree(build([]))))                        # []
print(level_order(solution.invertTree(build([1]))))                       # [1]
