from typing import List

class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.isEndOfWord = False

class StreamChecker:
    def __init__(self, words: List[str]):
        self.root = TrieNode()
        self.history = []
        for w in words:
            self.insert(w)
    
    def insert(self, word: str) -> None:
        curr = self.root
        for w in reversed(word):
            idx = ord(w) - ord('a')
            if curr.children[idx] is None:
                curr.children[idx] = TrieNode()
            curr = curr.children[idx]
        curr.isEndOfWord = True
        
    def query(self, letter: str) -> bool:
        self.history.append(letter)
        curr = self.root
        for i in range(len(self.history)-1, -1, -1):
            c = self.history[i]
            idx = ord(c) - ord('a')
            if curr.children[idx] is None:
                return False
            curr = curr.children[idx]
            if curr.isEndOfWord:
                return True
        return False