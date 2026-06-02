from typing import List, Counter

class Greedy:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        g = n-1
        for i in range(n-2, -1, -1):
          if nums[i] + i >= g:
              g = i
        return g == 0

    def jumpII(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 2:
            return 0
        c = 0
        curr_ = 0
        p = 0
        for i in range(n-2):
            p = max(p, i+nums[i])
            if curr_ == i:
                curr_ = p
                c += 1
                if curr_ >= n-1:
                    break
        return c


if __name__ == "__main__":
    sol = Greedy()
    print(f"\nJumping Sol: \n{sol.jumpII([4,1,1,3,1,1,1])}")