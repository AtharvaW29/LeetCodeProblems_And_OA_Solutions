from typing import List, Optional
from collections import defaultdict
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
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
    
    def pairSum(self, head: Optional[ListNode]) -> int:
        dummy = ListNode(0)
        dummy.next = head
        slow = dummy
        fast = head
        res = 0
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        secondHalf = slow.next
        slow.next = None
        prev = None
        while secondHalf:
            sec_next = secondHalf.next
            secondHalf.next = prev
            prev = secondHalf
            secondHalf = sec_next
        secondHalf = prev
        while secondHalf:
            res = max(res, head.val + secondHalf.val)
            head = head.next
            secondHalf = secondHalf.next
        return res

    def processStr(self, s: str, k: int) -> str:
        res:list = []
        n = len(s)
        lengths = [0] * n
        curr = 0
        for i, c in enumerate(s):
            if c == '*':
                if curr > 0:
                    curr -=1
            elif c == "#":
                curr *= 2
            elif c == "%":
                pass
            else:
               curr += 1
            lengths[i] = curr 
        if k >= curr:
            return '.'
        for i in reversed(range(n)):
            c = s[i]
            prev_sz = lengths[i-1] if i > 0 else 0

            if c == "*":
                continue
            elif c == "#":
                if k >= prev_sz:
                    k -= prev_sz
            elif c == "%":
                k = prev_sz - 1 - k
            else:
                if prev_sz == k:
                    return c
        return '.'

    def maxBuilding(self, n: int, restrictions: List[List[int]]) -> int:
        res_copy = restrictions.copy()
        res_copy.append([1, 0])
        res_copy.sort()
        if not res_copy or res_copy[-1][0] !=n:
            res_copy.append([n, n-1])
        k = len(res_copy)
        for i in range(1, k):
            crrH = res_copy[i-1][1] + (res_copy[i][0] - res_copy[i-1][0])
            res_copy[i][1] = min(res_copy[i][1], crrH)
        
        for i in range(k-2, 0, -1):
            crrH = res_copy[i+1][1] + (res_copy[i+1][0]-res_copy[i][0])
            res_copy[i][1] = min(res_copy[i][1], crrH)

        max_h = 0

        for i in range(k-1):
            left_h = res_copy[i][1]
            right_h = res_copy[i+1][1]
            dist = res_copy[i+1][0] - res_copy[i][0]
            h = (left_h + right_h + dist) // 2
            max_h = max(max_h, h)
        return max_h

    def maxIceCream(self, costs: List[int], coins: int) -> int:
        """
        Counting sort approach:
         - Count the frequency of each cost
         - Iterate through the costs in ascending order, buying as many as possible until coins run out
         - Return the total number of ice creams bought
         Time complexity: O(n + m) where n is the number of costs and m is the max cost
         Space complexity: O(m) for the counting array
        """
        max_range = max(costs) + 1
        counts = [0] * max_range
        res = [0] * len(costs)
        for num in costs:
            counts[num] += 1
        for i in range(1, len(counts)):
            counts[i] += counts[i-1]
        for num in reversed(costs):
            res[counts[num] -1] = num
            counts[num] -= 1
        i = 0
        while coins > 0 and i < len(res):
            if coins < res[i]:
                return i
            coins -= res[i]
            i += 1
        return i

    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        MOD = 1_000_000_000 + 7
        m = r - l + 1
        if n==1:
            return m
        dp_up = [0] * m
        dp_down = [0] * m
        # base case
        for y in range(m):
            dp_up[y] = y
            dp_down[y] = m-1-y
        # dp
        for _ in range(3, n+1):
            prefUp = [0] * (m+1)
            prefDown = [0] * (m+1)
            for j in range(m):
                prefUp[j+1] = (prefUp[j] + dp_up[j]) % MOD
                prefDown[j+1] = (prefDown[j] + dp_down[j]) % MOD
            new_dp_up = [0]*m
            new_dp_down = [0]*m
            total_up = prefUp[m]
            for y in range(m):
                new_dp_up[y] = prefDown[y]
                new_dp_down[y] = (total_up - prefUp[y+1]) % MOD
            dp_up = new_dp_up
            dp_down = new_dp_down
        return (sum(dp_up) + sum(dp_down)) % MOD

class ZigZagArraysII:
    MOD = 1_000_000_007

    def mat_mul(self, A, B):
        n = len(A)
        m = len(B[0])
        p = len(B)
        C = [[0] * m for _ in range(n)]
        for i in range(n):
            for k in range(p):
                if A[i][k] == 0:
                    continue
                aik = A[i][k]
                for j in range(m):
                    C[i][j] = (C[i][j] + aik * B[k][j]) % self.MOD
        return C

    def mat_pow(self, M, e):
        n = len(M)
        R = [[0] * n for _ in range(n)]
        for i in range(n):
            R[i][i] = 1
        while e:
            if e & 1:
                R = self.mat_mul(R, M)
            M = self.mat_mul(M, M)
            e >>= 1
        return R

    def mat_vec_mul(self, M, v):
        n = len(M)
        res = [0] * n
        for i in range(n):
            s = 0
            for j, val in enumerate(v):
                s = (s + M[i][j] * val) % self.MOD
            res[i] = s
        return res

    def zigZagArrays(self, n, l, r):
        m = r - l + 1
        if n == 1:
            return m

        size = 2 * m
        T = [[0] * size for _ in range(size)]

        for y in range(m):
            for x in range(y):
                T[y][m + x] = 1

        for y in range(m):
            for x in range(y + 1, m):
                T[m + y][x] = 1

        V2 = [0] * size
        for y in range(m):
            V2[y] = y
            V2[m + y] = m - 1 - y

        P = self.mat_pow(T, n - 2)
        Vn = self.mat_vec_mul(P, V2)
        return sum(Vn) % self.MOD

class Fenwick:
    def __init__(self, n:int):
        self.n = n
        self.bit  = [0] * (n+1)

    def update(self, i:int, delta:int) -> None:
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i
    
    def query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

class MajoritySubArrays:
    def countMajoritySubarrays(self, nums: List[int], target: int) -> int:
        n = len(nums)
        pref = 0
        res = 0
        offset = n + 1
        size = 2 * n + 3
        fw = Fenwick(size)
        fw.update(offset, 1)
        for v in nums:
            if v == target:
                pref += 1
            else:
                pref -= 1
            res += fw.query(pref + offset - 1)
            fw.update(pref+offset, 1)
        return res

    def maximumLength(self, nums: List[int]) -> int:
        freq = defaultdict(int)
        for n in nums: freq[n] += 1
        n = freq[1]
        ans = n if n%2 == 1 else max(0, n-1)
        for k in freq:
            if k == 1:
                continue
            size = 0
            crr = k
            while crr in freq and freq[crr] >= 2:
                size += 2
                crr *= crr
            if crr in freq and freq[crr] < 2:
                size += 1
            elif crr not in freq:
                size -= 1
            ans = max(ans, size)
        return ans