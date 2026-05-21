from typing import List

class IntervalType:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        res = []
        n = len(intervals)
        for i in range(n):
            if newInterval[0] > intervals[i][1]:
                # Does the newInterval go after the current one?
                res.append(intervals[i])
            elif newInterval[1] < intervals[i][0]:
                # Does the newInterval go before the current one?
                res.append(newInterval)
                res = res + intervals[i:]
                return res
            else:
                # if both conditions are false then we have an overlap
                newInterval = [min(newInterval[0], intervals[i][0]), max(newInterval[1], intervals[i][1])]
        res.append(newInterval) # edge case if intervals = [] and newInterval != []
        return res