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

        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)

        return 1 + max(left_depth, right_depth)

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None and q is None:
            return True
        if p is None or q is None:
            return False
        if p.val == q.val:
            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        return False

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.s = root.val
        # max_formula = root.val + left_path + right_path
        def max_sum(node: Optional[TreeNode]):
            if node is None:
                return 0

            left = max(0, max_sum(node.left))
            right = max(0, max_sum(node.right))

            temp = node.val + left + right
            self.s = max(self.s, temp)

            return node.val + max(left, right)
        max_sum(root)
        return self.s