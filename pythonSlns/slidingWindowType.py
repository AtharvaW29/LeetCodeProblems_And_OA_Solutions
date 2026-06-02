from collections import deque
from typing import List, Counter
from operator import itemgetter


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        dq = deque()
        n = len(nums)
        result = []

        for j in range(n):
            if dq and dq[0] == j - k:
                dq.popleft()

            while dq and nums[dq[-1]] <= nums[j]:
                dq.pop()

            dq.append(j)

            if j >= k - 1:
                result.append(nums[dq[0]])

        return result

    def findAnagrams(self, s: str, p: str) -> List[int]:
        a = len(s)
        b = len(p)
        result: List[int] = []
        pfreq = Counter[p]
        freq = Counter[s[:b]]

        for i in range(a - b + 1):
            if freq == pfreq:
                result.append(i)
            if i + b < a:
                new_ = s[i + b]
                freq[new_] += 1
                old_ = s[i]
                freq[old_] -= 1
                if freq[old_] == 0:
                    del freq[old_]

        return result

    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        current_sum = 0
        freq = {0: 1}
        for i in nums:
            current_sum += i
            if (current_sum - k) in freq:
                count += freq[current_sum - k]
            freq[current_sum] = freq.get(current_sum, 0) + 1

        return count

    def topKFrequent(self, nums: List[int], k: int) -> list[int]:
        freq = Counter[nums]
        sorted_freq = sorted(freq.items(), key=itemgetter(1), reverse=True)
        topK_freq = sorted_freq[:k]

        return [item[0] for item in topK_freq]


    def minMeetingRooms(self, intervals: List[Interval]) -> int:

        start = sorted([i.start for i in intervals])
        end = sorted([i.end for i in intervals])

        s, e = 0, 0
        res, count = 0, 0

        while s < len(intervals):
            if start[s] < end[e]:
                count += 1
                s += 1
            else:
                count -= 1
                e += 1
            res = max(res, count)

        return res


