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