#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import itertools
from random import shuffle
import random

Point = namedtuple("Point", ['i', 'x', 'y'])#index, x, y

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def totalDistance(tour, points, nodeCount, isPerm):
	if isPerm:
		d=0
	else:
		d = length(points[tour[-1]], points[tour[0]])
	for index in range(0, nodeCount-1):
		d += length(points[tour[index]], points[tour[index+1]])
	return d

def optimal(points, nodeCount, tour):
	opts = []
	inc = 7
	tries = 1
	bestTour = tour[:]
	best = 1000000000
	for i in range(tries):
		for step in range(0,nodeCount,inc):
			minDist = 1000000000
			for perm in itertools.permutations(tour[step:step+inc]):
				#print perm, totalDistance(perm[:], points, len(perm), False)
				if len(perm)<inc:
					d = totalDistance(tuple(list(perm[:])+tour[0:]), points, len(perm), True)
				else: 
					d = totalDistance(perm[:], points, len(perm), True)
				if d < minDist:
					minDist = d
					tour[step:step+len(perm)] = perm[:]
			#print step
		#print tour
		tourDistance = totalDistance(tour[:], points, nodeCount, False)
		#print tourDistance
		if tourDistance < best:
			bestTour = tour[:]
			best = tourDistance
			#print best
		shuffle(tour)
	return bestTour[:]

def spiral(points, nodeCount):
	tour = range(0, nodeCount)
	#return tour
	origin = Point(-1, 0,0)
	#SORT BY DISTANCE TO ORIGIN
	points = [p for p in sorted(points, key=lambda p: -length(origin, p))]
	
	#Start at farthest
	i = 0
	p1 = points[-1]
	tour[p1.i] = i
	while points:
		points.remove(p1)
		i+=1
		#rank
		nearest = [p2 for p2 in sorted(points, key=lambda p2: length(p1, p2))]
		if not nearest:
			break
		p1 = nearest[0]
		tour[p1.i] = i			
		
	return tour

def genSolution(points, nodeCount):
	tour = range(0, nodeCount)
	tour = optimal(points, nodeCount, tour)
	tour = twoOpt(points, nodeCount, tour)

	bestTour = tour[:]
	best = totalDistance(tour, points, nodeCount, False)

	for i in range(600):
		#2-opt descent. Change to sim annealing
		temp = twoOpt(points, nodeCount, tour)
		tempDist = totalDistance(temp, points, nodeCount, False)
		if tempDist<best:
			bestTour = temp[:]
			best = tempDist
			print best, i
			#print bestTour
	print "HIIII"

	tabu = []
	for k in range(2,5):
		print k
		for i in range(10000):
			nodes = sorted(random.sample(range(0,nodeCount),k))
			if nodes in tabu:
				i-=1
				continue
			tabu.append(nodes)
			temp = kOpt(points, nodeCount, bestTour[:], nodes)
			tempDist = totalDistance(temp, points, nodeCount, False)
			if tempDist<best:
				bestTour = temp[:]
				best = tempDist
				print best
				#print bestTour
	tabu = []
	for k in range(3,1,-1):
		print k
		for i in range(10000):
			nodes = sorted(random.sample(range(0,nodeCount),k))
			if nodes in tabu:
				i-=1
				continue
			tabu.append(nodes)
			temp = kOpt(points, nodeCount, bestTour[:], nodes)
			tempDist = totalDistance(temp, points, nodeCount, False)
			if tempDist<best:
				bestTour = temp[:]
				best = tempDist
				print best
				#print bestTour

	return bestTour

def shuffleLoop(points, nodeCount):
	tour = range(nodeCount)
	

def kOpt(points, nodeCount, tour, nodes):
	#Nodes to swap. K kwap
	#print 'nodes', nodes
	bestTour = tour[:]
	bestDist = totalDistance(bestTour, points, nodeCount, False)

	tabu = []
	for perm in itertools.permutations(map(lambda i: bestTour[i], nodes)):
		for i in range(0, len(nodes)):
			tour[nodes[i]] = perm[i]
		#Check if better
		if perm not in tabu:
			d = totalDistance(tour, points, nodeCount, False)
			tabu.append(perm)
		if  d < bestDist:
			bestTour = tour[:]
			bestDist = d
	return bestTour

def twoOpt(points, nodeCount, tour):
	#optimal(points, nodeCount)
	#return tour
	tabu = []
	#Has bug FIXXXXXX
	for i in range(1, len(tour)):
		best = [-1, 0]
		for j in range(1, len(tour)):
			if not j == i and j not in tabu:
				d1 = length(points[tour[i-1]], points[tour[i]])+length(points[tour[j-1]], points[tour[j]])
				d2 = length(points[tour[i-1]], points[tour[j]])+length(points[tour[j-1]], points[tour[i]])
				if d1-d2 > best[1]:
					#swap
					best = [j, d1-d2]
					#print best
					#tabu.append(j)
		if not best[0] == -1:
			tour[i], tour[best[0]] = tour[best[0]], tour[i]
	#print tour[1]
	return tour

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(int(i-1), float(parts[0]), float(parts[1])))
    
    solution = genSolution(points, nodeCount)

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

