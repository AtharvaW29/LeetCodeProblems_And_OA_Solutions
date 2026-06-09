from collections import OrderedDict, defaultdict
class ListNode:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

class LinkedList:
    def __init__(self):
        self.left = ListNode(0) # dummy node
        self.right = ListNode(0, self.left) # dummy node
        self.left.next = self.right
        self.map = {}
    
    def length(self):
        return len(self.map)
    
    def pushRight(self, value):
        node = ListNode(value, self.right.prev, self.right)
        self.map[value] = node
        self.right.prev = node
        node.prev.next = node
    
    def pop(self, value):
        if value in self.map:
            node = self.map[value]
            prev, next = node.prev, node.next
            prev.next = node.next
            next.prev = prev
            self.map.pop(value, None)
    
    def popLeft(self):
        res = self.left.next.value
        self.pop(self.left.next.value)
        return res

    def update(self, value):
        self.pop(value)
        self.pushRight(value)

class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.lfucount = 0
        self.counter_ = defaultdict(int)
        self.List = defaultdict(LinkedList)

    def counter(self, key):
        c = self.counter_[key]
        self.counter_[key] += 1
        self.List[c].pop(key)
        self.List[c+1].pushRight(key)

        if c == self.lfucount and self.List[c].length() == 0:
            self.lfucount += 1
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.counter(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        
        if key not in self.cache and len(self.cache) == self.capacity:
            val = self.List[self.lfucount].popLeft()
            self.cache.pop(val)
            self.counter_.pop(val)
        
        self.cache[key] = value
        self.counter(key)
        self.lfucount = min(self.lfucount,self.counter_[key] )