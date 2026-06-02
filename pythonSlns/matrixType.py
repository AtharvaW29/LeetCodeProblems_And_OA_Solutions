import sys
from typing import List, Optional
import math

class MatrixSolutions(object):

    def setZeroes(self, matrix: List[List[int]]) -> None:
        m = int(len(matrix))
        n = int(len(matrix[0]))
        mem = {}
        for i in range(0, m):
            for j in range(0, n):
                if matrix[i][j] == 0:
                    mem[(i, j)] = 0

        for r,c in mem.keys():
            print(f"\n {r}, {c}")
            for j in range(0, n):
                matrix[r][j] = 0

            for i in range(0, m):
                matrix[i][c] = 0

        print(f"\n FInally:--> {matrix}")



if __name__ == "__main__":
    msol = MatrixSolutions()
    matrix =  [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
    zeroes = msol.setZeroes(matrix)
    print(f"Results: {zeroes}")