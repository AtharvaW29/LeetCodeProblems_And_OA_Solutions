from typing import List
import heapq
class BinaryType(object):
    def getSum(self, a: int, b: int) -> int:
        mask = 0XFFFFFFFF
        while (b & mask) != 0:
            s = a ^ b
            car = (a & b) << 1
            a = s
            b = car
        return (a & mask) if b > 0 else a

    def hammingWeight(self, n: int) -> int:
        if n == 0: return 0
        b = 0
        while n > 0:
            if (n & 1):
                b += 1
            n >>= 1
        return b

    def reverseBits(self,n: int) -> int:
        if n == 0: return 0
        bits = f'{n:032b}'
        r = ""
        print(f"\n {bits}")
        for i in range(len(bits)-1, -1, -1):
            r += bits[i]
        print(f"\n {r}")

        return int(str(r), 2)

    def countBits(self, n: int) -> List[int]:
        """Conventional Approach"""
        res = []
        for i in range(n+1):
            s = f'{i:032b}'
            res.append(int(s.count('1')))
        """
        DP Approach
        res = [0] * (n+1)
        for i in range(1, n+1):
            res[i] = res[i >> 1] + (i & 1)
        :return res
        """
        return res

    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums) + 1
        return (n * (n-1))//2 - sum(nums)

if __name__ == "__main__":
    sol = BinaryType()
    res = sol.missingNumber([0,1,2,3,4,5,6,7,9])
    print(f"\n Results: {res}")

