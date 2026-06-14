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