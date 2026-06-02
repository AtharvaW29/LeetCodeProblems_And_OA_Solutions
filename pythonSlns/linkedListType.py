from typing import Optional, List
from collections import deque
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedListType:
        def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
            crr = head
            prev = None
            while crr:
                next_ = crr.next
                crr.next = prev
                prev = crr
                crr = next_
            return prev
        # Method II
        def reverseList2(self, head: Optional[ListNode]) -> Optional[ListNode]:
            def create_linked_list(arr):
                dummy = ListNode(0)
                crr = dummy
                for val in arr:
                    crr.next = ListNode(val)
                    crr = crr.next
                return dummy.next
            queue = deque()
            curr = head
            arr = []
            while curr:
                queue.append(curr.val)
                curr = curr.next
            while queue:
                arr.append(queue.pop())
            return create_linked_list(arr)

        def hasCycle(self, head:Optional[ListNode]) -> bool:
            visited = set()
            curr = head
            while curr:
                if curr in visited:
                    return True
                visited.add(curr)
                curr = curr.next
            return False
        # Method II
        def hasCycle2(self, head:Optional[ListNode]) -> bool:
            slow = head
            fast = head
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
                if slow == fast:
                    return True
            return False
        
        def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
            dummy = ListNode(0)
            crr = dummy
            while list1 and list2:
                if list1.val < list2.val:
                    crr.next = list1
                    list1 = list1.next
                else:
                    crr.next = list2
                    list2 = list2.next
                crr = crr.next

            if list1:
                crr.next = list1
            if list2:
                crr.next = list2
            
            return dummy.next

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
        
        def mergeKListsMethodII(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
            """Method II: O(NlogK) time complexity, O(1) space complexity"""
            arr = []
            dummy = ListNode(0)
            crr = dummy
            for i, node in enumerate(lists):
                if node:
                    heapq.heappush(arr, (node.val, i, node))
            while arr:
                val, i, node = heapq.heappop(arr)
                crr.next = ListNode(val)
                crr = crr.next
                if node.next:
                    heapq.heappush(arr, (node.next.val, i, node.next))
            return dummy.next
        
        def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
            dummy = ListNode(0)
            dummy.next = head
            slow = dummy
            fast = dummy
            for _ in range(n):
                fast = fast.next
            while fast.next is not None:
                slow = slow.next
                fast = fast.next
            slow.next = slow.next.next
            return dummy.next

        def reorderList(self, head: Optional[ListNode]) -> None:
            """
            Do not return anything, modify head in-place instead.
            """
            slow = head
            fast = head
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            secondhalf = slow.next
            slow.next = None
            prev = None
            while secondhalf:
                sec_next = secondhalf.next
                secondhalf.next = prev
                prev = secondhalf
                secondhalf = sec_next
            firsthalf = head
            secondhalf = prev
            while secondhalf:
                tmp_f = firsthalf.next
                tmp_s =  secondhalf.next
                firsthalf.next = secondhalf
                secondhalf.next = tmp_f
                firsthalf = tmp_f
                secondhalf = tmp_s
            return
        
        def reorderListMethodII(self, head: Optional[ListNode]) -> None:
            """
            Do not return anything, modify head in-place instead.
            """
            if not head:
                return
            q = deque()
            curr = head
            while curr:
                q.append(curr)
                curr = curr.next
            curr = q.popleft()
            while q:
                curr.next = q.pop()
                curr = curr.next
                if q:
                    curr.next = q.popleft()
                    curr = curr.next
            curr.next = None
                
            return

        def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
            if not head or not head.next:
                return None
            dummy = ListNode(0)
            dummy.next = head
            slow = dummy
            fast = head
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            slow.next = slow.next.next
            return dummy.next