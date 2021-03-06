#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
import numpy as np
from sortedcontainers import SortedSet, SortedDict
import itertools
import random

def nodeInvertedIndex(edges):
	#node: [edges]
	idx = defaultdict(SortedSet)#can change to numpy array following double growth resizing
	for i in range(len(edges)):
		idx[edges[i][0]].add(edges[i][1])
	return idx

def colorIndex(colors):
	#color: [node_ids]
	cdx = defaultdict(SortedSet)
	for i in range(len(colors)):
		cdx[colors[i]].add(i)
	#cdx = [cdx[key] for key in sorted(cdx, key=lambda key: -len(cdx[key]))]#sort biggest to smallest NO EFFECT Try kempe swap
	return cdx

def basicGreedy(edges, node_count):
    # build a trivial solution
    # every node has its own color
    return range(0, node_count)

def improvedGreedy(edges, node_count):
	# returns onePass greedy colors algorithm
	
	ndx = nodeInvertedIndex(edges)#actually node edge index
	colors = np.arange((node_count), dtype='uint16')
	return onePass(ndx, colors)

def greedyByDegree(edges, node_count):
	# returns onePass greedy colors algorithm on nodes sorted by degree
	ndx = nodeInvertedIndex(edges)
	colors = np.arange((node_count), dtype='uint16')
	return onePass(ndx, colors)
	'''
	ndx = nodeInvertedIndex(edges)#actually node edge index
	print ndx
	ndx = defaultdict(SortedSet)[{key: ndx[key]} for key in sorted(ndx, key=lambda key: -len(ndx[key]))]#sort biggest to smallest 
	print ndx
	colors = np.arange((node_count), dtype='uint16')
	return onePass(ndx, colors)'''

def greedyMultiPass(edges, node_count):
	ndx = nodeInvertedIndex(edges)
	colors = np.arange((node_count), dtype='uint16')
	return multiPass(ndx, colors)

def colorMultiPass(edges, node_count):
	ndx = nodeInvertedIndex(edges)
	colors = np.arange((node_count), dtype='uint16')
	return reduceColors(ndx, colors)

def swapConnColors(c1, c2, ndx):
	#kempe chain connected
	new1 = SortedSet()
	new2 = SortedSet()

	for i in c1:
		swapped = False
		for j in ndx[i]:
			if j in c2:
				new1.add(j)
				new2.add(i)
				swapped = True
		if not swapped:
			new1.add(i)
			new2.add(j)		
	#print c1, c2
	#print new1, new2
	return new1,new2		
	
def cArray(cdx, colors):
	for c in range(len(cdx)):
		for edge in cdx[c]:
			colors[edge] = c
	return colors

def kempeDescent(edges, node_count):
	#kempe chain neighborhood descent
	ndx = nodeInvertedIndex(edges)#actually node edge index
	colors = onePass(ndx, np.arange((node_count), dtype='uint16'))
	cdx = colorIndex(colors)
	
	print max(colors)+1
	#Gradient descent by kempe swap

	
	#Can select the swaps better
	best = np.copy(colors)#numpy uses pointers
	print max(best)+1
	for i,j in list(itertools.combinations(cdx.iterkeys(), 2)):
		print max(best)+1
		old_i = cdx[i]
		old_j = cdx[j]

		c0, c1 = swapConnColors(cdx[i],cdx[j], ndx)
		cdx[i] = c0
		cdx[j] = c1

		colors = onePass(ndx, cArray(cdx, colors))
		
		if max(colors) < max(best):			
			best = np.copy(colors)
		#can chain swaps
		elif max(colors) > max(best):
			#revert swap since worse
			cdx[i] = old_i
			cdx[j] = old_j

	return best

#TODO try k-opt untwisting

def onePass(ndx, colors):
	# Outputs feasible space algorithm.
	# 1 pass check neighbors and assign lowest color

	#keys = [key for key in sorted(ndx, key=lambda key: -len(ndx[key]))]#sort biggest to smallest 
	for i in sorted(ndx, key=lambda key: -len(ndx[key])):
		colors[i]=0
		j=0
		while j < len(ndx[i]):
			if colors[i] == colors[ndx[i][j]]:
				colors[i] += 1
				j=-1
			j+=1
	return colors

def reduceColors(ndx, colors):
	best = np.copy(onePass(ndx, colors))#runs degree greedy
	print max(best)+1

	stop = 0
	while stop < 10:
		cdx = colorIndex(best)
		#print cdx
	
		keys = [key for key in sorted(ndx, key=lambda key: len(ndx[key]))][:10]
		for i in keys:
			colors[i]=0
			j=0
			while j < len(ndx[i]):
				if colors[i] == colors[ndx[i][j]]:
					colors[i] += 1
					j=-1
				j+=1
		print max(colors)+1
		if max(colors) < max(best):
			best = np.copy(colors)
		stop+=1
	return best	

def multiPass(ndx, colors):
	best = np.copy(onePass(ndx, colors))#runs degree greedy
	print max(best)+1

	#while. Update best if better
	stop = 0
	while stop < 100:
		cdx = colorIndex(best)
		#print cdx
	
		keys = cdx.keys()
		random.shuffle(keys)
		#print keys
		for k in keys:
			for i in cdx[k]:
				colors[i]=0
				j=0
				while j < len(ndx[i]):
					if colors[i] == colors[ndx[i][j]]:
						colors[i] += 1
						j=-1
					j+=1
		if max(colors) < max(best):
			best = np.copy(colors)
		stop+=1
	return best	
		

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
	
    #solution = improvedGreedy(edges, node_count)
	#solution = basicGreedy(edges, node_count)
    #solution = greedyByDegree(edges, node_count)
    #solution = greedyMultiPass(edges, node_count)
    solution = colorMultiPass(edges, node_count)
    #solution = kempeDescent(edges, node_count)

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

