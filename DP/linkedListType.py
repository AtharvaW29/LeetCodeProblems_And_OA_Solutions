from typing import Optional
from collections import deque

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