#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def trivialGreedy(items, capacity):
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

	return value, taken

def weightedGreedy(items, capacity):
	value = 0
	weight = 0
	taken = [0]*len(items)
	
	#print items
	items = sorted(items, key=lambda item: float(item.value)/item.weight)
	#print items
	for item in items:
		if weight + item.weight <= capacity:
			taken[item.index] = 1
			value += item.value
			weight += item.weight
	return value, taken


def recursive(items, capacity):
	#dynamic without memoization. Computing taken impossible because of repeated calls.
	taken = [1]*len(items)
	def O(i, c, items):
		if i<0:
			return 0
		if items[i].weight<=c:
			without = O(i-1,c,items)
			added = O(i-1, c-items[i].weight,items)+items[i].value
			if added >= without:
				taken[items[i].index] = 1
				return added
			else:
				taken[items[i].index] = 0
				return without
		else:
			#taken[items[i].index] = 0
			return O(i-1,c,items)

	return O(len(items)-1, capacity, items), taken
	
def dynamic(items, capacity):
	taken = [0]*len(items)
	o = np.zeros((len(items)+1,capacity+1), dtype=np.int32)
	
	#i item index and c capacity index
	for k in range(1, len(o[:,0])):
		for c in range(1, len(o[0,:])):
			i = k-1
			if items[i].weight <= c:
				o[k,c]= max(o[k-1,c],o[k-1, c-items[i].weight]+items[i].value)
			else:
				o[k,c] = o[k-1,c]
	
	#Taken
	i = len(items)
	c=capacity
	while(i>0):
		if o[i, c] == o[i-1, c]:
			i -= 1
		elif o[i, c] > o[i-1, c]:
			taken[items[i-1].index] = 1
			c -= items[i-1].weight
			
	return o[len(items), capacity], taken

'''
A* or DFS https://class.coursera.org/optimization-003/forum/thread?thread_id=53
https://people.mpi-inf.mpg.de/~mehlhorn/ftp/Toolbox/GenericMethods.pdf
After sorting the items by decreasing density, place empty knapsack in priority queue. Remove top knapsack from queue, and add both that knapsack without the next item and with the next item, update pointer to the next item.
The evaluation function is the current value plus the heuristic estimate. Here we can use the optimistic estimate from knapsack lecture 5 on branch and bound -- the linear relaxation optimistic estimate.
'''

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))


	#value, taken = weightedGreedy(items, capacity)
    value, taken = dynamic(items, capacity)
	#print value#value1
    
    # prepare the solution in the specified output format

    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

