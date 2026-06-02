from typing import List, Optional
from collections import deque, defaultdict

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class GraphType:
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

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        if numCourses -1 == 0: return [0]

        adj = defaultdict(list)
        in_deg = [0] * numCourses
        
        for a, b in prerequisites:
            adj[b].append(a)
            in_deg[a] += 1
            
        queue = deque([i for i in range(numCourses) if in_deg[i] == 0])
        
        order = []
        
        while queue:
            prereq = queue.popleft()
            order.append(prereq)
            
            for course in adj[prereq]:
                in_deg[course] -= 1

                if in_deg[course] == 0:
                    queue.append(course)
        
        return order if len(order) == numCourses else []
    
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Minimum Height Trees
        The intuition is to find the midpoint of the tree
        such that it is almost equidistant from all the codes.
        This can be done by ignoring the leaves until only
        two nodes are left and by using a queue
        """
        if n <= 1: return [0]
        adj = defaultdict(set)
        in_deg = defaultdict(int)
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
            in_deg[a] += 1
            in_deg[b] += 1
        queue = deque([i for i in range(n) if in_deg[i] == 1])
        nodes = n
        while nodes > 2:
            leaves = len(queue)
            nodes -= leaves
            for i in range(leaves):
                l = queue.popleft()
                for neigh in adj[l]:
                    in_deg[neigh] -= 1
                    if in_deg[neigh] == 1:
                        queue.append(neigh)
        return list(queue)

    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        n = len(heights[0])  # cols
        m = len(heights)  # rows

        set_p = set()
        set_a = set()

        queue_p = deque()
        queue_a = deque()

        for i in range(m):
            queue_p.append([i, 0])
            set_p.add((i, 0))
            queue_a.append([i, n - 1])
            set_a.add((i, n - 1))
        for j in range(n):
            queue_p.append([0, j])
            set_p.add((0, j))
            queue_a.append([m - 1, j])
            set_a.add((m - 1, j))

        def bfs(queue, visited):
            while queue:
                ox, oy = queue.popleft()
                for dx, dy in [[0, 1], [1, 0], [-1, 0], [0, -1]]:
                    x = ox + dx
                    y = oy + dy
                    if 0 <= x < m and 0 <= y < n and (x, y) not in visited:
                        if heights[ox][oy] <= heights[x][y]:
                            queue.append([x, y])
                            visited.add((x, y))

        bfs(queue_p, set_p)
        bfs(queue_a, set_a)
        res = (set_p & set_a)

        return [list(item) for item in res]

    def numIslands(self, grid: List[List[str]]) -> int:
        if grid is None: return 0
        m = len(grid)
        n = len(grid[0])
        count = 0

        def dfs(i, j):
            queue = deque()
            if queue is None: return {}
            visited = set()
            queue.append([i,j])
            while queue:
                ox, oy = queue.popleft()
                grid[ox][oy] = '$'
                for dx, dy in [[0,1], [1, 0], [-1, 0], [0, -1]]:
                    x = ox + dx
                    y = oy + dy
                    if 0 <= x < m and 0 <= y < n and (x,y) not in visited:
                        if grid[x][y] == '1':
                            queue.append([x,y])
                            visited.add((x,y))

        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    dfs(i,j)
                    count += 1

        return count
    
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        adj = defaultdict(set)
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        state = set()
        def dfs(curr, prev):
            if curr in state:
                return True
            state.add(curr)
            for c in adj[curr]:
                if c == prev:
                    continue
                if dfs(c, curr):
                    return True
            return False
        dfs(0, -1)
        return len(state) == n

    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        """Count the number of connected components in an undirected graph
           This is an implementation of Disjoint Set Union (DSU) or Union-Find data structure 
           to count the number of connected components in an undirected graph. 
           The idea is to iterate through the edges and union the nodes that are connected. 
           After processing all edges, we can count the number of unique parents (or representatives) 
           to determine the number of connected components.
        """
        if len(edges) == 0:
            return n
        adj = defaultdict(set)
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)

        visited = [False] * n
        count = 0
        stack = []
        for i in range(n):
            if not visited[i]:
                count += 1
                visited[i] = True
                stack = [i]
                while stack:
                    a = stack.pop()
                    for c in adj[a]:
                        if not visited[c]:
                            visited[c] = True
                            stack.append(c)
        return count
