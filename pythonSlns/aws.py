from typing import List, Counter
import sys
import heapq
import math

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        freq = {}
        for i, v in enumerate(nums):
            c = target - v
            if c in freq:
                return [i, freq[c]]
            freq[c] = i

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n = len(nums) - 1
        res = []
        nums.sort()

        for i in range(n):
            if nums[i] == nums[i-1]:
                continue
            l, r = i+1, n
            while l < r:
                total = nums[i] + nums[l] + nums[r]
                if total < 0:
                    l += 1
                elif total > 0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    while nums[l] == nums[l-1] and l < r:
                        l += 1
        return res
    
    def maxProfit(self, prices: List[int]) -> int:
        minprice = float('inf')
        profit = 0
        for i in range(len(prices)):
            minprice = min(minprice, prices[i])
            profit = max(profit, prices[i] - minprice)
        return profit

    def lengthOfLongestSubstring(self, s: str) -> int:
        best = 0
        seen = {}
        l = 0
        for r, ch in enumerate(s):
            if ch in seen and seen[ch] >= l:
                l = seen[ch] + 1
            seen[ch] = r
            best = max(best, r - l +1)
        return best
    
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        if not nums: return 0
        l = 0
        current_sum = 0
        size = sys.maxsize
        for r in range(len(nums)):
            current_sum += nums[r]
            while current_sum >= target:
                size = min(size, r - l + 1)
                current_sum -= nums[l]
                l += 1
        return size if size != sys.maxsize else 0

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter[nums]
        heap = []

        for i, v in freq.items():
            if len(heap) < k:
                heapq.heappush(heap, (v, i))
            else:
                heapq.heappushpop(heap, (v, i))
        return [h[1] for h in heap]

    def isValid(self, s: str) -> bool:
        if len(s) % 2 != 0: return False
        stack = []
        bmap = {"(": ")", "[": "]", "{": "}", "#": "#"}
        for i in range(len(s)):
            if s[i] in bmap:
                top = stack.pop() if stack else '#'
                if s[i] != bmap[top]:
                    return False
            else:
                stack.append(s[i])
        return not stack

    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums: return 0
        if len(nums) == 1: return 1
        nums.sort()
        count = 0
        l, r = 0, 1
        res = []
        while r < len(nums):
            if nums[r] - nums[l] == 1:
                count += 1
            elif nums[r] - nums[l] > 1:
                count = 0
            res.append(count)
            l += 1
            r += 1

        return max(res) + 1

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = []
        zero_count = nums.count(0)
        total_prod_no_zeros = math.prod([x for x in nums if x != 0])

        for a in nums:
            if zero_count > 1:
                res.append(0)
            elif zero_count == 1:
                res.append(total_prod_no_zeros if a == 0 else 0)
            else:
                res.append(total_prod_no_zeros // a)

        return res

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:

        intervals.sort(key=lambda x: x[0])
        res = [intervals[0]]
        for s, e in intervals[1:]:
            last_end = res[-1][1]
            if s <= last_end:
                res[-1][1] = max(e, last_end)
            else:
                res.append([s, e])
        return res
