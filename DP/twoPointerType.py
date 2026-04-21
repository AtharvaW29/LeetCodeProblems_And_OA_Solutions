from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        res = 0
        while l < r:
            a = (r - l) * min(height[r], height[l])
            res = max(a, res)
            if height[l] > height[r]:
                r -= 1
            else:
                l += 1
        return res
