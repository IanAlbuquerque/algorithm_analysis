
NUM_VERTICES = 5

cost = [	[0,		1,			10,			100,			1000 		],		
			[1,		0,			10000,		100000,			1000000 	],		
			[10,	10000,		0,			10000000,		100000000 	],		
			[100,	100000,		10000000,	0,				1000000000	],		
			[1000,	1000000,	100000000,	1000000000,		0			]]

minCost = float('inf')
minPath = []

'''
numLeaves = 0
'''

def bruteForce(visited, toBeVisited, costSoFar, lowerBoundFunction):
	global cost
	global minCost
	global minPath
	global numLeaves
	# the current is the last node visited
	currentNode = visited[-1]

	if(len(toBeVisited) == 0):
		costTotal = costSoFar + cost[currentNode][0]

		'''
		print("....")
		print(visited)
		print(costTotal)
		numLeaves = numLeaves + 1
		'''

		if(costTotal <= minCost):
			minCost = costTotal
			minPath = list(visited)
		return

	else:

		arrayToSort = []

		for i in xrange(len(toBeVisited)):

			childNode = toBeVisited.pop(0) # pop front
			visited.append(childNode) # push back

			lowerBoundOfThatChild = lowerBoundFunction( visited, 
														toBeVisited,
														costSoFar+cost[currentNode][childNode])
			
			toBeVisited.append(childNode) # push back
			visited.pop() # pop back

			arrayToSort.append((childNode,lowerBoundOfThatChild))

		arraySorted = list(reversed(sorted(	arrayToSort, 
											key=lambda tupleChildLowerBound: tupleChildLowerBound[1])))

		toBeVisited = [int(tup[0]) for tup in arraySorted]

		for i in xrange(len(arraySorted)):

			childNode, lowerBoundOfThatChild = arraySorted.pop(0)
			visited.append(childNode) # push back

			toBeVisitedChild = [int(tup[0]) for tup in arraySorted]

			bruteForce(	visited,
						toBeVisitedChild,
						costSoFar+cost[currentNode][childNode],
						lowerBoundFunction)

			arraySorted.append((childNode, lowerBoundOfThatChild))
			visited.pop() # pop back

def initBruteForce(lowerBoundFunction):
	visited = [0]
	toBeVisited = []
	for i in xrange(1,NUM_VERTICES):
		toBeVisited.append(i)
	bruteForce(visited, toBeVisited, 0, lowerBoundFunction);

def main():
	initBruteForce()

	print("--------")
	print(minCost)
	print(minPath)

	'''
	print(numLeaves)
	'''

if __name__ == "__main__":
    main()