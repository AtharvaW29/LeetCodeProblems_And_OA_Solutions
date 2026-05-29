from typing import List, Optional
from collections import defaultdict
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Twitter:
    def __init__(self):
        self.count = 0
        self.following = defaultdict(set)
        self.post = defaultdict(list)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.post[userId].append([self.count, tweetId])
        self.count -= 1

    def getNewsFeed(self, userId: int) -> List[int]:
        res = []
        min_heap = []
        self.following[userId].add(userId)
        for followeeId in self.following[userId]:
            idx = len(self.post[followeeId]) - 1
            count, postId = self.post[followeeId][idx]
            heapq.heappush(min_heap, [count, postId, followeeId, idx - 1])
        heapq.heapify(min_heap)
        while min_heap and len(res) < 10:
            count, postid, followeeId, idx = heapq.heappop(min_heap)
            res.append(postid)
            if idx >= 0:
                next_count, next_postid = self.post[followeeId][idx]
                heapq.heappush(min_heap, [next_count, next_postid, followeeId, idx - 1])

        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if self.following:
            if followeeId in self.following.get(followerId):
                self.following[followerId].remove(followeeId)

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.scores = nums
        heapq.heapify(self.scores)
        while len(self.scores) > k:
            heapq.heappop(self.scores)

    def add(self, val:int) -> int:
        heapq.heappush(self.scores, val)
        if len(self.scores) > self.k:
            heapq.heappop(self.scores)

        return self.scores[0]
    
class HeapType:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        arr = []
        dummy = ListNode(0)
        crr = dummy
        for l in lists:
            while l:
                arr.append(l.val)
                l = l.next
        heapq.heapify(arr)
        while arr:
            crr.next = ListNode(heapq.heappop(arr))
            crr = crr.next
        return dummy.next
