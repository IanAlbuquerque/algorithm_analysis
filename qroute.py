'''
=============================================================================
CONSTANTS / INPUT OF THE PROBLEM
=============================================================================
'''

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
	A matrix where EDGE_WEIGHT[i][j] is the weight of the edge that connects the i-th vertex to
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
=============================================================================
ALGORITHM IMPLEMENTATION
=============================================================================
'''

'''
FUNCTION
	bruteForce
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
def bruteForce( list_nodes_visited,
				list_nodes_to_be_visited,
				cost_so_far,
				lowerBoundFunction):

	# Global variables potentially writen in this function.
	global min_cost_so_far
	global min_path_so_far
	global num_leaves_visited_so_far

	# The current node being "investigated" is the last node that has been visited
	current_node = list_nodes_visited[-1]

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

		print("....")
		print(list_nodes_visited)
		print(cost_total)
		num_leaves_visited_so_far = num_leaves_visited_so_far + 1

		# If the total cost of the current permutation is better than the one we had previously,
		# update the global variables min_cost_so_far and min_path_so_far
		if(cost_total <= min_cost_so_far):

			print("UPDATED MIN HERE!")

			min_cost_so_far = cost_total
			min_path_so_far = list(list_nodes_visited)

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
		list_tuples_ordered = list(reversed(sorted(	list_tuples_unordered, key=lambda tupleChildLowerBound: tupleChildLowerBound[1])))

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
			if(lower_bound_of_that_child <= min_cost_so_far):

				cost_of_that_child = cost_so_far + EDGE_WEIGHT[current_node][child_node]

				bruteForce(		list_nodes_visited, 
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

'''
FUNCTION
	initBruteForce
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
def initBruteForce(lowerBoundFunction):

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

	# Starts the recursion
	bruteForce( 	list_nodes_visited,
					list_nodes_to_be_visited,
					cost_initial_partial_permutation,
					lowerBoundFunction);

'''
=============================================================================
MAIN FUNCTION
=============================================================================
'''

def main():
	initBruteForce(zeroLowerBound)

	print("--------")
	print(min_cost_so_far)
	print(min_path_so_far)

	print(num_leaves_visited_so_far)

if __name__ == "__main__":
    main()