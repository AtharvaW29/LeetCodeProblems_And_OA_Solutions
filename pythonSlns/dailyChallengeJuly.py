from math import inf
from typing import List
from collections import deque
from itertools import pairwise

class UnionFind:
    def __init__(self, size):
        self.size = size
        self.parent = list(range(size))
    
    def find(self, i)->int:
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def unite(self, i, j)->bool:
        i_ = self.find(i)
        j_ = self.find(j)
        if i_ == j_:
            return False
        if i_ != j_:
            self.parent[i_] = j_
        return True
class SafestPathinaGrid:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return 0
        dist = [[inf] * n for i in range(n)]
        queue = deque()
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    dist[i][j] = 0
                    queue.append((i, j))
        dirs = (-1,0,1,0,-1)
        while queue:
            p, q = queue.popleft()
            for dx, dy in pairwise(dirs):
                x = dx + p
                y = dy + q
                if (0 <= x < n) and (0 <= y < n) and dist[x][y] == inf:
                    dist[x][y] = dist[p][q] + 1
                    queue.append((x, y))
        cells = []
        for i in range(n):
            for j in range(n):
                cells.append((dist[i][j], i, j))
        cells.sort(reverse=True)
        uf = UnionFind(n * n)
        for d, i, j in cells:
            for dx, dy in pairwise(dirs):
                x = dx + i
                y = dy + j
                if (0 <= x < n) and (0 <= y < n) and dist[x][y] >= d:
                    uf.unite(i * n + j, x * n + y)
            if uf.find(0) == uf.find(n * n - 1):
                return int(d)
        return 0