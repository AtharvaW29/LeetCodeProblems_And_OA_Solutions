from typing import List, Optional
from collections import defaultdict
import heapq

class SparseTable:
    def __init__(self, nums: List[int]):
        n = len(nums)
        bw = n.bit_length()
        self.min_ = [[0] * n for _ in range(bw)]
        self.max_ = [[0] * n for _ in range(bw)]

        for i in range(n):
            self.min_[0][i] = self.max_[0][i] = nums[i]

        for i in range(1, bw):
            step = 1 << (i - 1)
            span = 1 << i
            for j in range(n - span + 1):
                self.min_[i][j] = min(self.min_[i - 1][j], self.min_[i - 1][j + step])
                self.max_[i][j] = max(self.max_[i - 1][j], self.max_[i - 1][j + step])

    def query(self, left: int, right: int) -> int:
        if left >= right:
            return 0
        length = right - left
        k = length.bit_length() - 1
        mx = max(self.max_[k][left], self.max_[k][right - (1 << k)])
        mn = min(self.min_[k][left], self.min_[k][right - (1 << k)])
        return mx - mn

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class DailyChallengeJune:
    def minimumCost(self, cost: List[int]) -> int:
        total = 0
        cost.sort(reverse=True)
        for i in range(len(cost)):
            if (i+1) % 3 != 0:
                total += cost[i]
        return total
    def earliestFinishTime(self, landStartTime: List[int], landDuration: List[int], waterStartTime: List[int], waterDuration: List[int]) -> int:
    
        land_first = float('inf')
        water_first = float('inf')

        for l_strt, l_dur in zip(landStartTime, landDuration):
            l_fin = l_strt + l_dur
            for w_strt, w_dur in zip(waterStartTime, waterDuration):
                w_finish = max(w_strt, l_fin) + w_dur
                land_first = min(land_first, w_finish)
        for w_strt, w_dur in zip(waterStartTime, waterDuration):
            w_fin = w_strt + w_dur
            for l_strt, l_dur in zip(landStartTime, landDuration):
                l_finish = max(w_fin, l_strt) + l_dur
                water_first = min(water_first, l_finish)
        return min(land_first, water_first)
    
    def earliestFinishTimeMethodII(self, landStartTime: List[int], landDuration: List[int], waterStartTime: List[int], waterDuration: List[int]) -> int:
    
        land_first = 1000001
        water_first = 1000001

        lt = min([landStartTime[i] + landDuration[i] for i in range(len(landDuration))])
        wt = min([waterStartTime[i] + waterDuration[i] for i in range(len(waterDuration))])
        for j in range(len(waterDuration)):
            l_tmp = max(lt, waterStartTime[j]) + waterDuration[j]
            land_first = min(land_first, l_tmp)
        for j in range(len(landDuration)):
            w_tmp = max(wt, landStartTime[j]) + landDuration[j]
            water_first = min(water_first, w_tmp)
        return min(land_first, water_first)
    
    def earliestFinishTimeII(self, landStartTime: List[int], landDuration: List[int], waterStartTime: List[int], waterDuration: List[int]) -> int:
        def find_min(ride1StartTime: List[int], ride1Duration: List[int], ride2StartTime: List[int], ride2Duration: List[int]) -> int:
            res = float('inf')
            temp_min = float('inf')
            for r1s, r1d in zip(ride1StartTime, ride1Duration):
                temp_min = min(temp_min, r1s+r1d)
            for r2s, r2d in zip(ride2StartTime,ride2Duration):
                r2strt = max(temp_min, r2s) + r2d
                res = min(res, r2strt)
            return res
        
        land_f = find_min(landStartTime, landDuration, waterStartTime, waterDuration)
        water_f = find_min(waterStartTime, waterDuration, landStartTime, landDuration)
        return min(land_f, water_f)
    
    def leftRightDifference(self, arr: List[int]) -> List[int]:
        l, r = 0, sum(arr)
        def getdiff(i):
            nonlocal l, r
            r -= i
            res = abs(r - l)
            l += i
            return res
        return [getdiff(i) for i in arr]

    def createBinaryTree(self, descriptions: List[List[int]]) -> Optional[TreeNode]:
        treenodes = {}
        children = set()
        for parent, child, isLeft in descriptions:
            children.add(child)
            if parent not in treenodes:
                treenodes[parent] = TreeNode(parent)
            if child not in treenodes:
                treenodes[child] = TreeNode(child) 
            if isLeft == 1:
                treenodes[parent].left = treenodes[child]
            elif isLeft == 0:
                treenodes[parent].right = treenodes[child]
        res = (set(treenodes.keys()) - children).pop()
        return treenodes[res]

    def maxTotalValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0 or k == 0:
            return 0

        st = SparseTable(nums)

        # Max-heap via negative values:
        # ( -range_value, left, right )
        heap = [(-st.query(0, n), 0, n)]
        seen = {(0, n)}

        result = 0

        while heap and k > 0:
            neg_val, l, r = heapq.heappop(heap)
            val = -neg_val
            result += val
            k -= 1

            if l < r - 1:
                left_child = (l, r - 1)
                right_child = (l + 1, r)

                if left_child not in seen:
                    seen.add(left_child)
                    heapq.heappush(heap, (-st.query(*left_child), *left_child))

                if right_child not in seen:
                    seen.add(right_child)
                    heapq.heappush(heap, (-st.query(*right_child), *right_child))

        return result
    
    def assignEdgeWeights(self, edges: List[List[int]]) -> int:
        if not edges:
            return 0
        adj = defaultdict(set)
        children = set()
        MOD = 1_000_000_007
        for e in edges:
            p, c = e[0], e[1]
            children.add(c)
            adj[p].add(c)
        def depth(n, p, crr, adj):
            max_d = crr
            for neigh in adj[n]:
                if neigh != p:
                    max_d = max(max_d, depth(neigh, n, crr+1, adj))
            return max_d
        r = (set(adj.keys()) - children).pop()
        x = depth(r, -1, 0, adj) - 1
            
        return pow(2, x, MOD)

    def assignEdgeWeightsII(self, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        adj = defaultdict(list)
        MOD = 1_000_000_007
        for u,v in edges:
            adj[u].append(v)
            adj[v].append(u)
        n = len(edges) + 1
        pow_2 = [1] * (n+1)
        for i in range(1, n+1):
            pow_2[i] = (pow_2[i-1] * 2)%MOD

        log = n.bit_length() + 1
        depth = [0] * (n+1)
        up = [[0] * log for _ in range(n+1)]

        def dfs(node, par, d):
            depth[node] = d
            up[node][0] = par
            for i in range(1, log):
                up[node][i] = up[up[node][i-1]][i-1]
            for neighbor in adj[node]:
                if neighbor != par:
                    dfs(neighbor, node, d+1)
        dfs(1,1,0)

        def lca(u, v):
            if depth[u] < depth[v]:
                u, v = v, u
            diff = depth[u] - depth[v]
            for i in range(log):
                if(diff >> i) & 1:
                    u = up[u][i]
            if u == v:
                return u
            for i in range(log-1, -1, -1):
                if up[u][i] != up[v][i]:
                    u = up[u][i]
                    v = up[v][i]
            return up[u][0]
        res = []
        for x,y in queries:
            if x==y:
                res.append(0)
            else:
                lca_ = lca(x, y)
                chain_length = depth[x] + depth[y] - 2*depth[lca_]
                res.append(pow_2[chain_length-1])
        return res

    def mapWordWeights(self, words: List[str], weights: List[int]) -> str:
        out = []
        for w in words:
            total = 0
            for c in w:
                total += weights[ord(c) - 97]
            out.append(chr(ord('z') - (total % 26)))
        return ''.join(out)