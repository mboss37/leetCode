# Practice script: docs/exercise_scripts/LC104_MaximumDepthBinaryTree_practice.md

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
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # Recursion. The depth of any subtree is:
        #   1 (for the root itself) + max(depth of left, depth of right)
        # Empty tree → 0.

        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


# ============= TEST HELPERS =============
def build(values):
    """Build a tree from level-order list. Use None for missing nodes."""
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


# ============= TEST CASES =============
solution = Solution()

print(solution.maxDepth(build([3, 9, 20, None, None, 15, 7])))   # 3
print(solution.maxDepth(build([1, None, 2])))                     # 2
print(solution.maxDepth(build([])))                                # 0
print(solution.maxDepth(build([1])))                               # 1
print(solution.maxDepth(build([1, 2, 3, 4, 5])))                  # 3
