from typing import List

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