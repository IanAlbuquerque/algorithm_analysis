import math

import time
import sys

import numpy
import skimage.io
import skimage.draw
'''
=============================================================================
CONSTANTS / INPUT OF THE PROBLEM
=============================================================================
'''

TIME_TO_RUN_ALGORITHM_IN_SECONDS = 60

'''
CONSTANT
	PATH_OUTPUT_FILE
DESCRIPTION:
	The path to the output file of the algorithm
'''
PATH_OUTPUT_FILE = "out.txt"
CITIES = []

'''
CONSTANT
	NUM_VERTICES
DESCRIPTION:
	The total number of vertices in the complete graph
'''
NUM_VERTICES = 5

'''
CONSTANT
	EDGE_WEIGHT
DESCRIPTION:
	A matrix where EDGE_WEIGHT[i][j] is the weight of the edge that connects the i-th 	vertex to
	the j-th vertex.
	Vertices start on 0.
	The graph should be undirected. Hence, EDGE_WEIGHT[i][j] = EDGE_WEIGHT[j][i] for every i and j.
	This matrix should be symmetric.
	Also, EDGE_WEIGHT[i][i] = 0. (The diagonal should be filled with zeros)
	Should have size NUM_VERTICES by NUM_VERTICES
	Also assumes positive values for every edge.
'''
EDGE_WEIGHT = [	[0,		1,			10,			100,			1000 		],		
				[1,		0,			10000,		100000,			1000000 	],		
				[10,	10000,		0,			10000000,		100000000 	],		
				[100,	100000,		10000000,	0,				1000000000	],		
				[1000,	1000000,	100000000,	1000000000,		0			]]

'''
=============================================================================
GLOBAL VARIABLES USED BY THE ALGORITHM
=============================================================================
'''

start_time_in_seconds = 0

'''
VARIABLE
	min_cost_so_far
DESCRIPTION:
	The total cost of the lowest-cost permutation found so far in the brute force algorithm.
	This is an UPPER BOUND for the solution of the problem.
'''
min_cost_so_far = float('inf')

'''
VARIABLE
	min_path_so_far
DESCRIPTION:
	The list, in order, of the vertices of the best (lowest-cost) permutation found so far.
'''
min_path_so_far = []

'''
=============================================================================
DEBUG VARIABLES
=============================================================================
'''

'''
VARIABLE
	num_leaves_visited_so_far
DESCRIPTION:
	The number of leaves visited in the algorithm so far.
	For debug purposes.
'''
num_leaves_visited_so_far = 0

'''
=============================================================================
LOWER BOUND IMPLEMENTATIONS
=============================================================================
'''

'''
FUNCTION
	zeroLowerBound
DESCRIPTION:
	The simplest lower bound possible (zero)
PARAMETERS:
	list_nodes_visited
		The list of visited vertices so far in that partial permutation
	list_nodes_to_be_visited
		The list of vertices that have not been visited yet in that partial permutation
	cost_so_far
		The cost so far of the edges that connect the vertices in that partial permutation
RETURNS
	0
		This function always return zero because zero is always a lower bound for this problem,
		given that all the edges are positive
'''
def zeroLowerBound(list_nodes_visited, list_nodes_to_be_visited, cost_so_far):
	return 0

'''
FUNCTION
	sumMinEdgesBound
DESCRIPTION:
	The cost of the partial permutation so far added to the sum of the lowest k edges
	of the graph, being k the number of nodes to be visited plus one.
	This is a lower bound for the total cost of permutations that start with the given
	partial permutation.
PARAMETERS:
	list_nodes_visited
		The list of visited vertices so far in that partial permutation
	list_nodes_to_be_visited
		The list of vertices that have not been visited yet in that partial permutation
	cost_so_far
		The cost so far of the edges that connect the vertices in that partial permutation
RETURNS
	an integer
		The cost of the partial permutation so far added to the sum of the lowest k edges
		of the graph, being k the number of nodes to be visited plus one.
GLOBAL VARIABLES USED:
	TO READ:
		NUM_VERTICES
		EDGE_WEIGHT
'''
def sumMinEdgesBound(list_nodes_visited, list_nodes_to_be_visited, cost_so_far):

	list_of_edge_costs = []
	for i in xrange(NUM_VERTICES):
		for j in xrange(i+1, NUM_VERTICES):
			list_of_edge_costs.append(EDGE_WEIGHT[i][j])
		# END FOR
	# END FOR

	list_of_edge_costs_sorted = sorted(list_of_edge_costs)

	lower_bound = cost_so_far
	for i in xrange(len(list_nodes_to_be_visited) + 1):
		lower_bound = lower_bound + list_of_edge_costs_sorted[i]
	# END FOR

	return lower_bound

def minimumTreeBound(list_nodes_visited, list_nodes_to_be_visited, cost_so_far):
	if len(list_nodes_to_be_visited) == 0:
		return EDGE_WEIGHT[list_nodes_visited[0]][list_nodes_visited[-1]] + cost_so_far

	mst_cost, mst = primMST(list_nodes_to_be_visited)

	min_start = min([EDGE_WEIGHT[list_nodes_visited[0]][x] for x in list_nodes_to_be_visited])
	min_end = min([EDGE_WEIGHT[list_nodes_visited[-1]][x] for x in list_nodes_to_be_visited])

	lower_bound = cost_so_far + mst_cost + min_start + min_end
	return lower_bound

def primMST(list_nodes):
	if len(list_nodes) == 0:
		return 0, []

	minimum_spanning_tree = [[list_nodes[-1],list_nodes[-1]]]
	cheapest_cost_list = []
	tree_cost = 0

	for i in xrange(len(list_nodes)-1):
		cheapest_cost_list.append([list_nodes[i], EDGE_WEIGHT[list_nodes[i]][list_nodes[-1]], list_nodes[-1]])

	while len(cheapest_cost_list) is not 0:
		x = min(cheapest_cost_list, key=lambda x: x[1])
		tree_cost += x[1]
		minimum_spanning_tree.append([x[0],x[2]])
		cheapest_cost_list.remove(x)

		for v in cheapest_cost_list:
			if EDGE_WEIGHT[x[0]][v[0]] < v[1]:
				v[1] = EDGE_WEIGHT[x[0]][v[0]]
				v[2] = x[0]

	return tree_cost, minimum_spanning_tree

'''
FUNCTION
	qRouteLowerBound
DESCRIPTION:
	This function returns the cost of a path that starts on vertex zero, follows the
	permutation path until the last vertex of the list_nodes_visited, goes to a vertex in the list_nodes_to_be_visited,
	does a q-route including only vertices of list_nodes_to_be_visited, and goes back
	to vertex number zero.

	This function returns the size of the smallest of those paths.

	Let N be the size of the list list_nodes_to_be_visited.
	The cost of going from vertex zero to the last vertex of the permutation is cost_so_far.
	For the rest of the costs, we may calculate the q route among the list_nodes_visited initializing
	the cost of the q route with zero edges starting on each vertex v as being the cost of the edge
	that connects v to the vertex 0, instead of the usual flat zero.
	Then, we calculate the q route with (N-1) vertices among list_nodes_to_be_visited.
	In the end, we do one more iteration to calculate q-routes starting on the last vertex
	of the partial permutation to the vertices in list_nodes_to_be_visited.
PARAMETERS:
	list_nodes_visited
		The list of visited vertices so far in that partial permutation
	list_nodes_to_be_visited
		The list of vertices that have not been visited yet in that partial permutation
	cost_so_far
		The cost so far of the edges that connect the vertices in that partial permutation
RETURNS
	an integer
		The size of the smallest of the paths described in the description
GLOBAL VARIABLES USED:
	TO READ:
		NUM_VERTICES
		EDGE_WEIGHT
'''
def qRouteLowerBound(list_nodes_visited, list_nodes_to_be_visited, cost_so_far):

	num_vertices_to_be_visited = len(list_nodes_to_be_visited)
	q_values_route_n_edges = []
	q_values_route_n_minus_1_edges = []
	vertices_in_table = []
	last_vertex_in_permutation = list_nodes_visited[-1]

	if num_vertices_to_be_visited == 0:
		return cost_so_far + EDGE_WEIGHT[last_vertex_in_permutation][0]
	# END IF

	for i in xrange(num_vertices_to_be_visited):
		vertex = list_nodes_to_be_visited[i]
		vertices_in_table.append(vertex)
		q_values_route_n_edges.append( EDGE_WEIGHT[vertex][0] );
	# END FOR

	for k in xrange(num_vertices_to_be_visited - 1):

		q_values_route_n_minus_1_edges = list(q_values_route_n_edges)

		for i in xrange(num_vertices_to_be_visited):
			source_vertex = vertices_in_table[i]
			q_values_route_n_edges[i] = float("inf")
			for j in xrange(num_vertices_to_be_visited):
				child_vertex = vertices_in_table[j]
				q_values_route_n_edges[i] = min(q_values_route_n_edges[i], EDGE_WEIGHT[source_vertex][child_vertex] + q_values_route_n_minus_1_edges[j])
			# END FOR
		# END FOR

	# END FOR

	smallest_q_route = float("inf")
	for i in xrange(num_vertices_to_be_visited):
		vertex = vertices_in_table[i]
		smallest_q_route = min( smallest_q_route, EDGE_WEIGHT[last_vertex_in_permutation][vertex] + q_values_route_n_edges[i] )

	lower_bound = smallest_q_route + cost_so_far

	return lower_bound

'''
=============================================================================
ALGORITHM IMPLEMENTATION
=============================================================================
'''

'''
FUNCTION
	bruteForceWithPrunning
DESCRIPTION:
	This is a recursive function.
	Runs the brute force of all permutations starting in a already defined partial permutation.
	This partial permutation is defined by the parameters: visited, to_be_visited and cost_so_far
	This function generates the rest of the permutations missing, and stores in the global variables
	min_cost_so_far and min_path_so_far any permutation that has a lower cost than the values previously
	present in those variables.
PARAMETERS:
	list_nodes_visited
		The list of visited vertices so far in that partial permutation
	list_nodes_to_be_visited
		The list of vertices that have not been visited yet in that partial permutation
	cost_so_far
		The cost so far of the edges that connect the vertices in that partial permutation
	lowerBoundFunction
		The lower bound function to be used. This function should receive as parameters the following:
				list_nodes_visited
					The list of visited vertices so far in that partial permutation
				list_nodes_to_be_visited
					The list of vertices that have not been visited yet in that partial permutation
				cost_so_far
					The cost so far of the edges that connect the vertices in that partial permutation
RETURNS
	<nothing>
GLOBAL VARIABLES USED:
	TO READ:
		EDGE_WEIGHT
	TO WRITE:
		min_cost_so_far
		min_path_so_far
		num_leaves_visited_so_far
'''
MAX_COUNT = 20000
COUNT = 0
def bruteForceWithPrunning( list_nodes_visited,
							list_nodes_to_be_visited,
							cost_so_far,
							lowerBoundFunction):

	# Global variables potentially writen in this function.
	global min_cost_so_far
	global min_path_so_far
	global num_leaves_visited_so_far
	global COUNT

	time_elapsed_in_seconds = time.time() - start_time_in_seconds
	if(time_elapsed_in_seconds > TIME_TO_RUN_ALGORITHM_IN_SECONDS):
		sys.exit();

	# The current node being "investigated" is the last node that has been visited
	current_node = list_nodes_visited[-1]

	COUNT = COUNT + 1
	if COUNT > MAX_COUNT:
		print list_nodes_visited
		print "Upper Bound = " + str(min_cost_so_far)
		print "Time Elapsed (Seconds) =" + str(time_elapsed_in_seconds)
		COUNT = 0

	# -----------------------
	# CASE 1) IS A LEAF (BASE CASE)
	# -----------------------
	# Checks if the current node is a leaf of the permutation tree.
	# A node is a leaf if there are no more vertices to be visited.
	if(len(list_nodes_to_be_visited) == 0):

		# cost_total is the total cost of that permutation.
		# It is the cost_so_far added to the weight of the edge of the last node to the first node.
		# This is necessary to conclude the cycle.
		cost_total = cost_so_far + EDGE_WEIGHT[current_node][0]

		num_leaves_visited_so_far = num_leaves_visited_so_far + 1

		# If the total cost of the current permutation is better than the one we had previously,
		# update the global variables min_cost_so_far and min_path_so_far
		if(cost_total < min_cost_so_far):

			min_cost_so_far = cost_total
			min_path_so_far = list(list_nodes_visited)

			file_out = open(PATH_OUTPUT_FILE,"a")
			file_out.write("-----------\n")
			file_out.write("Permutation = " + str(min_path_so_far) + "\n")
			file_out.write("Cost = " + str(min_cost_so_far) + "\n")
			file_out.write("Time Elapsed (seconds) = " + str(time_elapsed_in_seconds) + "\n")
			file_out.close()

			min_x = min(CITIES, key = lambda t: t[1])[1]
			min_y = min(CITIES, key = lambda t: t[2])[2]
			max_x = max(CITIES, key = lambda t: t[1])[1]
			max_y = max(CITIES, key = lambda t: t[2])[2]
			max_d = max(max_x - min_x, max_y - min_y)
			image = numpy.zeros( (1200, 1200) )
			for city in CITIES:
				rr, cc = skimage.draw.circle( 100+int((city[1] - min_x)*1000/max_d), 100+int((city[2] - min_y)*1000/max_d), 5)
				image[rr, cc] = 1
			for  i in xrange(1,NUM_VERTICES):
				city_end = CITIES[list_nodes_visited[i]]
				city_start = CITIES[list_nodes_visited[i-1]]
				rr, cc = skimage.draw.line(100+int((city_start[1] - min_x)*1000/max_d), 100+int((city_start[2] - min_y)*1000/max_d), 100+int((city_end[1] - min_x)*1000/max_d), 100+int((city_end[2] - min_y)*1000/max_d))
				image[rr, cc] = 1
			city_end = CITIES[list_nodes_visited[NUM_VERTICES-1]]
			city_start = CITIES[list_nodes_visited[0]]
			rr, cc = skimage.draw.line(100+int((city_start[1] - min_x)*1000/max_d), 100+int((city_start[2] - min_y)*1000/max_d), 100+int((city_end[1] - min_x)*1000/max_d), 100+int((city_end[2] - min_y)*1000/max_d))
			image[rr, cc] = 1
			image = 1.0 - image
			skimage.io.imsave(PATH_OUTPUT_FILE+str(min_cost_so_far)+".png",image)


		# END IF
		return
	#END IF

	# -----------------------
	# CASE 2) IS NOT A LEAF (RECURSION)
	# -----------------------
	# The current partial permutation is NOT a leaf:
	else:

		# -----------------------
		# STEP 1: SORT THE LIST OF CHILDREN BY LOWERBOUND (DESCENDING ORDER)
		# -----------------------

		# We will store in this array tuples (child, lower bound) where
		# child will be every child of the current node and
		# lower bound will the lower bound of that child 
		list_tuples_unordered = []

		# Iterates through every child
		# Specifically, iterates N times, where N is the number of children
		for i in xrange(len(list_nodes_to_be_visited)):

			# Picks the first child of the list of nodes to be visited. This is our child node.
			# Also, to generate the list of nodes visited for that child, appends the child node to
			# the list of nodes visited of the current node.
			child_node = list_nodes_to_be_visited.pop(0) 	# pop front
			list_nodes_visited.append(child_node) 			# push back

			# The cost of the partial permutation of the child will be the cost so far added to the edge
			# that connect the current node to the child.
			# Then, we can just call the lowerBound Funcion provided.
			cost_of_that_child = cost_so_far + EDGE_WEIGHT[current_node][child_node]

			lower_bound_of_that_child = lowerBoundFunction( 	list_nodes_visited, 
																list_nodes_to_be_visited,
																cost_of_that_child)
			
			# Now, we need to recover the list of nodes to be visited and the list of nodes already visited.
			# Since we are picking children from the front of the list to be visited, we can just
			# push the already iterated child to the back of the list, like a QUEUE
			# Also, since we pushed the child in the back of the list already visited,
			# we can just pop the child out of the list, like a STACK
			list_nodes_to_be_visited.append(child_node) # push back
			list_nodes_visited.pop() 					# pop back

			# Concatenated the new tuple to the list of tuples
			list_tuples_unordered.append( (child_node,lower_bound_of_that_child) )

		# END FOR

		# Sort the list of tuples by the second entry, that is the lower bound.
		# Also, make sure it is reversed, so we have higher lower bounds first.
		list_tuples_ordered = list((sorted(	list_tuples_unordered, key=lambda tupleChildLowerBound: tupleChildLowerBound[1])))

		# -----------------------
		# STEP 2: ITERATE THROUGH SORTED CHILDREN, POSSIBLY PRUNNING SUB-TREES
		# -----------------------

		# Iterates through every tuple previously obtained and sorted
		for tuple_element in list_tuples_ordered:

			# Recovers the members of the tuple: the child and its lower bound
			child_node, lower_bound_of_that_child = tuple_element

			# To build the lists of nodes visited and to be visited of the child,
			# we remove that child from the list to be visited
			# and add it to the end the list of nodes already visited
			list_nodes_to_be_visited.remove(child_node) 	# removes the first (and only) occurence of child_node
			list_nodes_visited.append(child_node) 			# push back

			# DO THE PRUNNING
			# We will only continue with the permutations by descending into the child if the lower bound
			# of that child is smaller (or equal) the upper bound so far, that is the cost
			# of the best permutation found so far.
			# That is, if the lower bound of that child is greater than the upper bound that we have,
			# there is no point in continuing to descend in that branch.
			if(lower_bound_of_that_child < min_cost_so_far):

				cost_of_that_child = cost_so_far + EDGE_WEIGHT[current_node][child_node]

				bruteForceWithPrunning(		list_nodes_visited, 
											list_nodes_to_be_visited, 
											cost_of_that_child, 
											lowerBoundFunction)

			# END IF

			# To recover the list of nodes visited and to be visited of the current node,
			# we undo the changes made before.
			# We add the child of the nodes to be visited to end of its list
			# and remove it from the nodes already visited
			# (from the end, since we added to the end, like a STACK)
			list_nodes_to_be_visited.append(child_node) 	# push back
			list_nodes_visited.pop() 						# pop back

	return

'''
FUNCTION
	initBruteForceWithPrunning
DESCRIPTION:
	This is the first call of a recursive function.
	Starts the brute force algorithm with the prunning on the first node (node zero) of the complete graph.
PARAMETERS:
	lowerBoundFunction
		The lower bound function to be used. This function should receive as parameters the following:
				list_nodes_visited
					The list of visited vertices so far in that partial permutation
				list_nodes_to_be_visited
					The list of vertices that have not been visited yet in that partial permutation
				cost_so_far
					The cost so far of the edges that connect the vertices in that partial permutation
RETURNS
	<nothing>
GLOBAL VARIABLES USED:
	TO READ:
		NUM_VERTICES
		EDGE_WEIGHT
	TO WRITE:
		min_cost_so_far
		min_path_so_far
		num_leaves_visited_so_far
'''
def initBruteForceWithPrunning(cities, costMatrix, lowerBoundFunction, output_file):

	# Global variables potentially writen in this function.
	global min_cost_so_far
	global min_path_so_far
	global num_leaves_visited_so_far
	global EDGE_WEIGHT
	global NUM_VERTICES
	global PATH_OUTPUT_FILE
	global CITIES
	global start_time_in_seconds

	start_time_in_seconds = time.time()

	CITIES = cities
	PATH_OUTPUT_FILE = output_file
	EDGE_WEIGHT = costMatrix
	NUM_VERTICES = len(costMatrix)

	file_out = open(PATH_OUTPUT_FILE,"w")
	file_out.write("BEST PERMUTATIONS FOUND SO FAR\n")
	file_out.close()

	# For the beginning, only node zero, the root, has already been visited
	list_nodes_visited = [0]

	# All the other nodes have not been visited yet.
	# For that, we iterate through all of them, adding them to this list.
	list_nodes_to_be_visited = []
	for i in xrange(1,NUM_VERTICES):
		list_nodes_to_be_visited.append(i)
	# END FOR

	# The permutation with only the vertex zero has no cost
	cost_initial_partial_permutation = 0

	# Initialize Global Variables
	min_cost_so_far = float('inf')
	num_leaves_visited_so_far = 0
	min_path_so_far = []

	# Starts the recursion
	bruteForceWithPrunning( 	list_nodes_visited,
								list_nodes_to_be_visited,
								cost_initial_partial_permutation,
								lowerBoundFunction);


def reportNumberPermutations():
	return math.factorial(NUM_VERTICES-1)

def reportLowestCost():
	return min_cost_so_far

def reportLowestCostPath():
	return min_path_so_far

def reportNumberOfLeavesVisisted():
	return num_leaves_visited_so_far

def reportPruningPercentage():
	number_of_possible_permutations = math.factorial(NUM_VERTICES-1)
	return (1.0 - float(num_leaves_visited_so_far)/float(number_of_possible_permutations))*100.0
'''
=============================================================================
MAIN FUNCTION
=============================================================================
'''

def main():

	number_of_possible_permutations = math.factorial(NUM_VERTICES-1)

	print("--------")
	print "NUMBER OF POSSIBLE PERMUTATIONS = " + str(number_of_possible_permutations)

	initBruteForceWithPrunning(zeroLowerBound)
	print("--------")
	print "LOWER BOUND USED: Zero Lower Bound"
	print "Lowest Cost = " + str(min_cost_so_far)
	print "Correspondent Permutation = " + str(min_path_so_far)
	print "Number of Leaves Visited = " + str(num_leaves_visited_so_far)
	print "Percentage of Permutations prunned = " + str((1.0 - float(num_leaves_visited_so_far)/float(number_of_possible_permutations))*100.0) + "%"

	initBruteForceWithPrunning(sumMinEdgesBound)
	print("--------")
	print "LOWER BOUND USED: Sum Min Edges"
	print "Lowest Cost = " + str(min_cost_so_far)
	print "Correspondent Permutation = " + str(min_path_so_far)
	print "Number of Leaves Visited = " + str(num_leaves_visited_so_far)
	print "Percentage of Permutations prunned = " + str((1.0 - float(num_leaves_visited_so_far)/float(number_of_possible_permutations))*100.0) + "%"

	initBruteForceWithPrunning(qRouteLowerBound)
	print("--------")
	print "LOWER BOUND USED: Q Route"
	print "Lowest Cost = " + str(min_cost_so_far)
	print "Correspondent Permutation = " + str(min_path_so_far)
	print "Number of Leaves Visited = " + str(num_leaves_visited_so_far)
	print "Percentage of Permutations prunned = " + str((1.0 - float(num_leaves_visited_so_far)/float(number_of_possible_permutations))*100.0) + "%"

if __name__ == "__main__":
    main()