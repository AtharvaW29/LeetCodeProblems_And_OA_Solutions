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
    
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        res = []
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        res.append(sorted_intervals[0])
        for s, e in sorted_intervals[0:]:
            last_e = res[-1][1]
            if s <= last_e:
                res[-1][1] = max(e, last_e)
            else:
                res.append([s, e])
        return res
    
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        count = 0
        sorted_intervals = sorted(intervals, key=lambda x: x[1])
        temp_e = -float('inf')
        for s, e in sorted_intervals:
            if s >= temp_e:
                temp_e = max(e, temp_e)
            else:
                count += 1               
        return count