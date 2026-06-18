from typing import List

class StudyPlanOneFifty:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        p = m-1
        q = n-1 
        r = m+n-1
        while r > 0:
            if nums1[p] < nums2[q]:
                nums1[r] = nums2[q]
                r -= 1
                q -= 1
            elif nums1[p] >= nums2[q]:
                tmp = nums1[r]
                nums1[r] = nums1[p]
                nums1[p] = tmp
                p -= 1
                r -= 1
            else:
                r -= 1