#!/usr/bin/env python2.7
from __future__ import print_function
import sys
import math
import prunning

def readFile(filepath):
    f = open(filepath)

    line  =  f.readline()
    while not line.startswith('NODE_COORD_SECTION'):
        if line.startswith('DIMENSION'):
            header, nItems = line.split(':')
            nItems = int(nItems)
        line =  f.readline()

    items = []

    for i in xrange(nItems):
        city, x, y = f.readline().split()
        items.append([int(city), float(x), float(y)])

    return items

def constructCostMatrix(items):
    costMatrix = []

    for i in xrange(len(items)):
        costMatrix.append([0]*len(items))
        for j in xrange(i+1):
            distance = calculateDistance(items[i], items[j])
            costMatrix[i][j] = distance
            costMatrix[j][i] = distance

    return costMatrix


def calculateDistance(cityInfoA, cityInfoB):
    if cityInfoB[0] == cityInfoA[0]:
        return 0
    return int(math.sqrt((cityInfoA[1]-cityInfoB[1])**2 + (cityInfoA[2]-cityInfoB[2])**2)+0.5)

def printMatrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])

def main():
    if len(sys.argv) != 3:
        print("!Uso: tsp.py {filepath} {numero algoritmo}")
        return
    
    script, filename, algorithm = sys.argv
    items = readFile(filename)
    costMatrix = constructCostMatrix(items)

    printMatrix(costMatrix)

    algorithm = int(algorithm)

    if algorithm == 1:
        prunning.initBruteForceWithPrunning(costMatrix, prunning.zeroLowerBound)
    elif algorithm == 2:
        prunning.initBruteForceWithPrunning(costMatrix, prunning.sumMinEdgesBound)
        
        
    # elif algorithm == 3:

    prunning.reportNumberPermutations()
    prunning.reportLowestCost()
    prunning.reportLowestCostPath()
    prunning.reportNumberOfLeavesVisisted()
    prunning.reportPruningPercentage()
        

if __name__ == "__main__":
    main()