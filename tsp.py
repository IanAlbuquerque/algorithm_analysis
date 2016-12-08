#!/usr/bin/env python3
import sys
import math

def readFile(filepath):
    f = open(filepath)

    line  =  f.readline()
    while not line.startswith('NODE_COORD_SECTION'):
        if line.startswith('DIMENSION'):
            header, nItems = line.split(':')
            nItems = int(nItems)
        line =  f.readline()

    items = []

    for i in range(nItems):
        city, x, y = f.readline().split()
        items.append([int(city), float(x), float(y)])

    return items

def constructCostMatrix(items):
    costMatrix = []

    for i in range(len(items)):
        costMatrix.append([0]*len(items))
        for j in range(i+1):
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

    # if algorithm == 1:
        
    # elif algorithm == 2:
        
    # elif algorithm == 3:
        

if __name__ == "__main__":
    main()