import sys
from typing import List, Optional
import math

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution(object):

    def coinChange(self, coins, amount):
        """Memoized Approach for the coin Change Problem
           Time Complexity = O(S * N)
           where S is number of coins and N is the amount
        """

        memo = {}

        def recurCoinChange(amount, coins, memo):
            if amount == 0: return 0

            if amount < 0: return -1

            if amount in memo:
                return memo[amount]

            minCoins = sys.maxsize

            for coin in coins:
                result = recurCoinChange(amount - coin, coins, memo)

                if result != -1:
                    minCoins = min(minCoins, result + 1)

            memo[amount] = minCoins if minCoins != sys.maxsize else -1

            return memo[amount]

        res = recurCoinChange(amount, coins, memo)
        return res

    def coinChangeBottomup(self, coins, amount):
        """
        Bottom Up Pass Approach for the Coin Change Problem
        Time Complexity = O(S * N)
        This approach is faster as it avoids recursion
        :param coins:
        :param amount:
        :return:
        """
        # Initialization Step
        dp = [amount + 1] * (amount + 1)
        # Base Case
        dp[0] = 0
        # 2d Array loop with recurrence relation
        for i in range (1, amount + 1):
            for coin in coins:
                if i >= coin:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] <= amount else -1

    # Length of Longest Sub sequence
    def lengthOfLIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # Initialization
        dp = [1] * (len(nums) + 1)

        # Base Case
        dp[0] = 1
        dp[1] = 1

        if len(nums) > 1:
            for i in range (1, len(nums)):
                for j in range (0, i):
                    if nums[j] < nums[i]:  # Internal Condition inside the loop
                        dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)

    # House Robbery Problem
    def rob(self, nums: List[int]) -> int:

        if len(nums) == 1: return nums[0]
        if len(nums) == 2: return max(nums)

        dp = [0] * (len(nums) + 1)
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        if len(nums) > 2:
            for i in range(2, len(nums)):
                dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])
        return max(dp)

    def rob2(self, nums: List[int]) -> int:
        """
        In this case the houses are circular
        Meaning the first and the last  are adjacent
        :param nums:
        :return:
        """
        if len(nums) == 1: return nums[0]
        if len(nums) == 2: return max(nums)

        def robdef(nums):
            if len(nums) == 1: return nums[0]
            if len(nums) == 2: return max(nums)

            dp = [0] * (len(nums) + 1)
            dp[0] = nums[0]
            dp[1] = max(nums[0], nums[1])
            if len(nums) > 2:
                for i in range(2, len(nums)):
                    dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])
            return max(dp)

        leaving_last = robdef(nums[:-1])
        including_last = robdef(nums[1:])
        return max(leaving_last, including_last)

    def robThree(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node: return [0,0]

            left_results = dfs(node.left)
            right_results = dfs(node.right)

            include_current = node.val + left_results[1] + right_results[1]
            exclude_current = max(left_results[0], left_results[1]) + max(right_results[0], right_results[1])

            return[include_current, exclude_current]

        result_include_root, result_exclude_root = dfs(root)
        return max(result_include_root, result_exclude_root)

    def moneyinthebank(self, cases: List[int], K) -> int:
        """
        :param K: int
        :param cases: List[int]
        :rtype: int
        """
        if len(cases) == 1: return cases[0] if cases[0] < K else 0
        if len(cases) == 2: return max(cases) if max(cases) < K else 0

        # Initialization
        n = len(cases)
        dp = [[0 for _ in range(K+1)] for _ in range(n+1)]

        # Base Case Initialization
        for j in range (K + 1):
            if len(cases) > 0:
                if cases[0] < j:
                    dp[0][j] = cases[0]
            if len(cases) > 1:
                if cases[1] < j:
                    dp[1][j] = cases[1]
                else:
                    dp[1][j] = 0
        # Recurrence equation
        for i in range(2, n + 1):
            for j in range(K + 1):
                dp[i][j] = dp[i-1][j]
                if cases[i-1] <= j:
                    dp[i][j] = max(dp[i][j], dp[i-2][j - cases[i-1]] + cases[i-1])
        return dp[n][K]
    def balloonproblem(self, loons: List[int]) -> int:
        """
        :param loons:
        :return: int
        """
        if len(loons) == 0 : return 0
        if len(loons) == 1 : return loons[0]
        n= len(loons)
        loons = [1] + loons + [1]

        dp = [[0] * (n+2) for _ in range(n+2)]

        for L in range(2, n+2):
            for i in range(0, n+2 - L):
                j = i + L
                for k in range(i+1, j):
                    c = dp[i][k] + loons[i] * loons[k] * loons[j] + dp[k][j]
                    dp[i][j] = max(dp[i][j], c)
        return dp[0][n+1]


    def marblesproblem(self, marbles: List[int]) -> int:
        """
        :param marbles:
        :return: int
        """
        if len(marbles) == 0 : return 0
        if len(marbles) == 1 : return marbles[0]

        n = len(marbles)
        dp = [[0] * (n+1) for _ in range(n+1)]

        # Base Case
        for i in range (n):
            dp[i][i] = marbles[i]

        # prefix sum
        pf_sum = sum(marbles)
        print(f"Total Sum of given marbles: {pf_sum}")

        for L in range(2, n+1):
            for i in range(0, n-L+1):
                j = i + L - 1
                pick_left = pf_sum - dp[i+1][j]
                pick_right = pf_sum - dp[i][j-1]
                dp[i][j] = max(pick_left, pick_right)
                if pick_left > pick_right:
                    pf_sum = pf_sum - pick_left
                if pick_right > pick_left:
                    pf_sum = pf_sum - pick_right

        return dp[0][n-1]


    def bandproblem(self, members: List[int]) -> int:
        """
        :param members:
        :return: int
        """
        if len(members) == 0 : return 0
        if len(members) == 1 : return 0

        n = len(members)
        # Base Case Initialization for both lists will be 1
        lis = [1] * (n+1)
        lds = [1] * (n+1)

        # First let's compute the longest increasing subsequence for the given members
        for i in range(1, n):
            for j in range(0, i):
                if members[j] < members[i]:
                    lis[i] = max(lis[i], lis[j] + 1)
        # Now let's compute the longest decreasing subsequence for the given members
        for i in reversed(range(n)):
            for j in range(i+1, n):
                if members[j] < members[i]:
                    lds[i] = max(lds[i], lds[j] + 1)
        # Now we find the longest mountain type sequence
        mx = 0
        for b in range(n+1):
            crr = (lis[b] + lds[b] - 1)
            mx = max(mx, crr)

        # Minimum number of people to remove = n - mx
        return n - mx

    def subseqsumhighestnoncon(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [0] * (n+1)
        dp[0] = nums[0]
        dp[1] = max(dp[0], nums[1])
        for i in range(2, n):
            dp[i] = max(dp[i-2] + nums[i], dp[i-1])
        return dp[n-1]

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        if n == 1: return nums
        # if n == 2: return max(nums)
        if k == 1: return nums
        # dp[nums][k]
        dp = [[-math.inf for _ in range(0, n + 1)] for _ in range(0, n + 1)]

        # Base Cases
        for b in range(n):
            dp[b][1] = nums[b]

        result: List[int] = []

        for j in range(2, k + 1):
            for i in range(j - 1, n):
                dp[i][j] = (max(dp[i - 1][j - 1], nums[i]))

        for i in range(n):
            for j in range(k + 1):
                print(dp[i][j], end=" ")
            print()

        print(f"Left to Right: {result}")

        for i in range(k - 1, n):
            result.append(dp[i][k])

        return result

    def makesquare(self, matchsticks: List[int]) -> bool:
        # We split the sides into four groups L, T, R, and B
        # I am constructing a Brute-Force Tree and using a DP Approach
        #  To reach a solution
        n = len(matchsticks)
        matchsticks.sort(reverse=True)
        total = sum(matchsticks)
        if total % 4 != 0:
            return False

        side = total // 4
        sides = [0] * 4

        # base case:
        if matchsticks[0] > side:
            return False

        # Recursive function for backtracking (over the matchsticks array)
        def dp(used):
            if used == n:
                return True
            # A loop for iterating over the sides array
            for i in range(4):

                if sides[i] + matchsticks[used] <= side:
                    sides[i] += matchsticks[used]
                    if dp(used + 1):
                        return True
                    sides[i] -= matchsticks[used]
            return False

        return dp(0)

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        k = len(s)  # size of the knapsack
        sack = k
        dp = [[0 for _ in range(k + 1)] for _ in range(k + 1)]
        for i in range(k + 1):
            dp[i][0] = 0
        for j in range(k + 1):
            dp[0][j] = 0

        for i in range(0, k):
            a = s[:i - 1]
            if a in wordDict:
                k -= i
            for w in range(1, k):
                print('')

        return True if k == 0 else False

    def numDecodings(self, s: str) -> int:
        if s is None or len(s) == 0: return 0

        if int(s[0]) == 0: return 0

        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1

        for i in range(2, n + 1):
            if s[i - 1] != '0':
                dp[i] += dp[i - 1]
            x = int(s[i - 2:i])
            if 10 <= x <= 26:
                dp[i] += dp[i - 2]

        return dp[n]

    def uniquePaths(self, m:int, n:int)-> int:
        if m is None or n is None:
            return 0
        dp = [[1 for _ in range(n + 1)] for _ in range(m + 1)]
        for i in range(m):
            dp[i][1] = 1
        for j in range(n):
            dp[1][j] = 1
        for i in range(m):
            for j in range(n):
                if dp[i+1][j]:
                    dp[i][j] = dp[i][j] + dp[i+1][j]
                if dp[i][j+1]:
                    dp[i][j] = dp[i][j] + dp[i][j+1]

        return dp[m-1][n-1]

    def combinationSum4(self, nums: List[int], target: int) -> int:
        if target == 0: return 0
        memo = {}
        memo[0] = 1
        for i in range(1, target+1):
            memo[i] = 0
            for n in nums:
                s = i - n
                if s < 0:
                    continue
                memo[i] = memo[i] + memo[s]
        return memo[target]

    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 0 or nums is None: return False
        dp = [False for _ in range(n)]
        dp[n-1] = True
        for i in range(n-2, -1, -1):
            f = min(n-1, i + nums[i])
            for j in range(i+1, f+1):
                if dp[j]:
                    dp[i] = True
                    break
        print(f"\n {dp}")
        return dp[0]

if __name__ == "__main__":
    print("Function is running as main")
    sol = Solution()
    loons = [1, 8, 6, 3, 6]
    k = 50000
    a = sol.uniquePaths(3, 2)
    print('Result for Unique Paths')
    print(f'\n{a}')




