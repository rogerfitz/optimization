#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
import numpy as np
from sortedcontainers import SortedSet

def nodeInvertedIndex(edges):
	idx = defaultdict(SortedSet)#can change to numpy array
	for i in range(len(edges)):
		idx[edges[i][0]].add(edges[i][1])
	return idx

def basicGreedy(edges, node_count):
    # build a trivial solution
    # every node has its own color
    return range(0, node_count)

def improvedGreedy(edges, node_count):
	# returns onePass greedy colors algorithm
	
	ndx = nodeInvertedIndex(edges)#actually node edge index
	colors = np.arange((node_count), dtype='uint16')
	return onePass(ndx, colors)

def onePass(ndx, colors):
	# Outputs feasible space algorithm.
	# 1 pass check neighbors and assign lowest color
	for i in range(len(colors)):
		colors[i]=0
		j=0
		while j < len(ndx[i]):
			if colors[i] == colors[ndx[i][j]]:
				colors[i] += 1
				j=-1
			j+=1
	return colors

def localKempe(edges, node_count):

	pass

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        edges.append((int(parts[1]), int(parts[0])))
	
    solution = improvedGreedy(edges, node_count)
	#solution = basicGreedy(edges, node_count)

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

