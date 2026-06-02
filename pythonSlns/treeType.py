from typing import Optional, List

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

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        if root is None or k is None:
            return 0
        count = 0
        res = None
        def inorder(node, count, k):
            if node is None or k is None:
                return count, None
            count, res = inorder(node.left, count, k)
            if res is not None:
                return count, res
            count += 1
            if count == k:
                return count, node.val

            return inorder(node.right, count, k)
        count, res = inorder(root, count, k)
        return res

    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        res = []
        def inorder(root, res):
            if root is None:
                return res
            res = inorder(root.left, res)
            res.append(root.val)
            return inorder(root.right, res)
        res = inorder(root, res)
        return res