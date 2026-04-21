from typing import List, Optional
from collections import deque, defaultdict

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Solution:
    def foreignDictionary(self, words: List[str]) -> str:
        adj = {c: set() for w in words for c in w}
        visited = {}
        result = []
        for j in range(len(words) - 1):
            w1, w2 = words[j], words[j + 1]
            minLen = min(len(w1), len(w2))
            if len(w1) > len(w2) and w1[: minLen] == w2[: minLen]: return ""

            for i in range(minLen):
                if w1[i] != w2[i]:
                    adj[w1[i]].add(w2[i])
                    break

        def dfs(c):
            if c in visited:
                return visited[c]

            visited[c] = True
            for neig in adj[c]:
                if dfs(neig):
                    return True
            visited[c] = False
            result.append(c)

        for c in adj:
            if dfs(c):
                return ""

        result.reverse()
        return "".join(result)

    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])
        mins, fresh = 0, 0
        queue = deque()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    fresh += 1
                if grid[r][c] == 2:
                    queue.append([r, c])
        print(f"Size of fresh: {fresh}")
        while queue and fresh > 0:
            for i in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if(nr < 0 or nr == rows or
                        nc < 0 or nc == cols or
                        grid[nr][nc] != 1):
                        continue
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append([nr, nc])
            mins += 1
        print(f"Size of final fresh: {fresh}")

        return mins if fresh == 0 else -1

    def __init__(self):
        self.visited = {}
        
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None
        if node.val in self.visited:
            return self.visited[node.val]
        nnode = Node(val = node.val)
        self.visited[nnode.val] = nnode
        nnode.neighbors = [self.cloneGraph(c) for c in node.neighbors]
        return nnode

    def cloneGraphApproachTwo(self, node: Optional['Node']) -> Optional['Node']:
        if node is None: return None
        newmap = {}
        def clone(node):
            if node in newmap: return newmap[node]
            copy = Node(node.val)
            newmap[node] = copy
            for n in node.neighbors:
                copy.neighbors.append(clone(n))
            return copy
        return clone(node) if node is not None else []

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj = defaultdict(list)
        n = numCourses
        in_deg = [0] * n
        for u, v in prerequisites:
            adj[u].append(v)
            in_deg[v] += 1
        queue = deque([i for i in range(n) if in_deg[i] == 0])
        topo_order = []
        pnc = 0
        while queue:
            u = queue.popleft()
            topo_order.append(u)
            pnc += 1

            for v in adj[u]:
                in_deg[v] -= 1
                if in_deg[v] == 0:
                    queue.append(v)
        if pnc == n:
            return True

        else:
            return False