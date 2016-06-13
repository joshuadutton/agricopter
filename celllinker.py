# This module finds for a graph of cells a
# relatively optimized complete covereage path
# for the drone, crossing from cell to cell
# only by existing edges

import time
from random import shuffle

import shapely
from shapely.geometry import Polygon

import decompose
import cellgrapher

# The total amount of time the algorithm will have to 
# look for an optimal path
TOTAL_TIME = 2

def optimal(start_cell, cells):
	"""
	This is the wrapper method in the optimal/optimal_helper method pair.
	optimal(), given a starting cell, will determine at least one complete
	coverage path starting at that cell and traversing the entire graph of
	cells. At each fork it randomly shuffles the edges so as to simulate
	an exhaustive search in lieu of a fully polished algorithm. It returns
	the shortest of all paths where length is the number of elements in
	each list.

	start_cell: a CellNode object as defined in decompose.py, that is
	            part of a graph generated by cellgrapher.py
	cells: a list of all the cells in the graph (CellNodes)
	Returns: a list of CellNode objets that may be followed by the
	         drone in that order

	TODO: Consider possibility of making 'stacks' a set and each
	      'stack' an immutable and thus hashable tuple
	"""
	stacks = []

	# start_time: to keep track of how much of the alloted time has
	# passed
	start_time = time.time()

	# While there is still some time left keep finding complete coverage paths
	while True:
		stack = []
		optimal_helper(start_cell, stack)
		stacks.append(stack)

		# Mark every node visited = False for further iterations and
		# coverage paths
		optimal_cleanup(cells)

		# break if we are out of time
		if (time.time() - start_time) > TOTAL_TIME:
			break

	# return the minimum-length stack
	return min(stacks, key=len)

def optimal_helper(node, stack):
	"""
	This is the recursive method in the optimal/optimal_helper method pair.
	Accepts: node - the CellNode from which to start searching for the 
			 coverage path.
			 stack - an empty list meant to hold the complete coverage path
	Alters:  stack - every time a node which has not been visited is found
	Returns: The number of times the path passes back through a cell that
	         had already been visited (note that these extraneous passes
	         through cells are NOT added to the stack). This includes passing
	         through cells to return to the starting position.
	"""
	# We've found an unvisited node, so mark it as visited and
	# append it to the stack
	node.visited = True
	stack.append(node)

	# For the current node, shuffle its edges to simulate, in
	# conjunction with multiple passes from the same starting 
	# node, an exhaustive search.
	shuffle(node.edges)

	extraneous_visits = 0

	# For each of the current node's edges, check if the corresponding
	# neighbor has been visited. If it hasn't, call optimal_helper()
	# recursively on that neighbor.
	for edge in node.edges:
		next_node = get_neighbor(node, edge)

		# If the node has never been visited before, recurse with
		# next_node as the base node
		if next_node.visited is False:
			extraneous_visits += optimal_helper(next_node, stack)

			# The path passes back through this cell, either as a transition
			# to another unvisited cell or as part of the return home.
			extraneous_visits += 1

	# Note that optimal_helper() will only return when this node has no
	# unvisited neighbors. If this is the outermost call to optimal_helper(),
	# every node in the graph has been visited.
	return extraneous_visits

# Utility method to mark each node as visited = False.
def optimal_cleanup(nodes):
	for node in nodes:
		node.visited = False

# Utility method to determine which node referenced in edge
# is a neighbor to the passed in node.
def get_neighbor(node, edge):
	if edge.node_a == node:
		return edge.node_b
	else:
		return edge.node_a
