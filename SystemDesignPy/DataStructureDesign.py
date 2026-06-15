import random
from collections import defaultdict

class RandomizedSet:
    def __init__(self):
        self.store = {}
        self.list = []
    def insert(self, val: int) -> bool:
        if val in self.store:
            return False
        else:
            self.store[val] = len(self.list)
            self.list.append(val)
            return True

    def remove(self, val: int) -> bool:
        if val not in self.store:
            return False
        else:
            idx = self.store[val]
            last = self.list[-1]
            self.list[idx] = last
            self.store[last] = idx
            self.list.pop()
            del self.store[val]
            return True

    def getRandom(self) -> int:
        return random.choice(self.list)
    
class RandomizedCollection:
    def __init__(self):
        self.store = defaultdict(set)
        self.list = []
    
    def insert(self, val: int) -> bool:
        state = len(self.store[val]) > 0
        self.store[val].add(len(self.list))
        self.list.append(val)
        return not state

    def remove(self, val: int) -> bool:
        if val not in self.store or not self.store[val]:
            return False
        idx = self.store[val].pop()
        last = self.list[-1]
        self.list[idx] = last
        self.store[last].add(idx)
        self.store[last].discard(len(self.list) - 1)
        self.list.pop()
        return True

    def getRandom(self) -> int:
        return random.choice(self.list) if self.list else 0
    
# All O(1) Data Structure with Linkedlist and Hashmap
class ListNode():
    def __init__(self, bucket):
        self.bucket = bucket
        self.keys = set()
        self.prev = None
        self.next = None

class AllOne:
    def __init__(self):
        self.key_map = {}
        self.bucket_map = {}
        self.head = ListNode(0)
        self.tail = ListNode(0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def inc(self, key: str) -> None:
        crr_bucket = 0
        new_bucket = 1
        if key in self.key_map:
            node = self.key_map[key]
            crr_bucket = node.bucket
            new_bucket = crr_bucket + 1
            node.keys.remove(key)
        
        if new_bucket not in self.bucket_map:
            new_node = ListNode(new_bucket)
            crr_node = self.bucket_map.get(crr_bucket, self.head)
            new_node.prev = crr_node
            new_node.next = crr_node.next
            crr_node.next.prev = new_node
            crr_node.next = new_node
            self.bucket_map[new_bucket] = new_node

        new_node = self.bucket_map[new_bucket]
        new_node.keys.add(key)
        self.key_map[key] = new_node

        crr_node = self.bucket_map.get(crr_bucket, self.head)
        if crr_node.bucket!=0 and len(crr_node.keys)==0:
                crr_node.prev.next = crr_node.next
                crr_node.next.prev = crr_node.prev
                del self.bucket_map[crr_bucket]
        return None

    def dec(self, key: str) -> None:
        if key not in self.key_map:
            return None
        node = self.key_map[key]
        crr_bucket = node.bucket
        new_bucket = crr_bucket-1
        node.keys.remove(key)
        
        if new_bucket == 0:
            del self.key_map[key]
        else:
            if new_bucket not in self.bucket_map:
                new_node = ListNode(new_bucket)
                crr_node = self.bucket_map.get(crr_bucket, self.head)
                new_node.prev = crr_node.prev
                new_node.next = crr_node
                crr_node.prev.next = new_node
                crr_node.prev = new_node
                self.bucket_map[new_bucket] = new_node
                    
            new_node = self.bucket_map[new_bucket]
            new_node.keys.add(key)
            self.key_map[key] = new_node
        crr_node = self.bucket_map.get(crr_bucket, self.head)
        if len(crr_node.keys) == 0 and crr_node.bucket != 0:
            crr_node.prev.next = crr_node.next
            crr_node.next.prev = crr_node.prev
            del self.bucket_map[crr_bucket]
        return None

    def getMaxKey(self) -> str:
        if self.head.next == self.tail:
            return ""
        if not self.tail.prev.keys:
            return ""
        
        return next(iter(self.tail.prev.keys))

    def getMinKey(self) -> str:
        if self.head.next == self.tail:
            return ""
        if not self.head.next.keys:
            return ""
        return next(iter(self.head.next.keys))