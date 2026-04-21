from typing import List

class ArrayType:
    # search in a rotated sorted array
    def search(self,nums: List[int], target: int) -> int:
        if nums is None or len(nums) == 0:
            return -1
        if target not in nums:
            return -1
        l, r = 0, len(nums) -1
        while l <= r:
            m = (r+l) // 2
            if nums[m] == target:
                return m
            elif nums[l] <= nums[m]:
                if nums[l] <= target < nums[m]:
                    r = m-1
                else:
                    l = m+1
            elif nums[r] >= nums[m]:
                if nums[m] < target <= nums[r]:
                    l = m+1
                else:
                    r = m-1
        return -1

    def findMin(self, nums: List[int]) -> int:
        """
        Find minimum in rotated sorted array-I
        :param nums:
        :return: int
        """
        if nums is None or len(nums) == 0:
            return 0
        l, r = 0, len(nums)-1
        if nums[l] <= nums[r]:
            return nums[0]
        while l < r:
            m = (r+l)//2
            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m
        return nums[l]

    def findMinII(self, nums: List[int]) -> int:
        if nums is None or len(nums) == 0:
            return -1
        l, r = 0, len(nums) - 1
        cl, cr = 0, len(nums) - 1
        if nums[l] < nums[r]:
            return nums[l]

        while l < r:
            m = (l + r) // 2
            if nums[m] > nums[r]:
                l = m + 1
            elif nums[m] < nums[r]:
                r = m
            else:
                r -= 1

        while cl < cr:
            cm = (cl + cr) // 2
            if nums[cm] < nums[cl]:
                cr = cm
            elif nums[cm] > nums[cr]:
                cl = cm + 1
            else:
                cl += 1

        return min(nums[l], nums[cl])
