#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple

Point = namedtuple("Point", ['i', 'x', 'y'])#index, x, y

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def spiral(points, nodeCount):
	visited = range(0, nodeCount)
	#return visited
	origin = Point(-1, 0,0)
	#SORT BY DISTANCE TO ORIGIN
	points = [p for p in sorted(points, key=lambda p: -length(origin, p))]
	
	#Start at farthest
	i = 0
	p1 = points[-1]
	visited[p1.i] = i
	while points:
		points.remove(p1)
		i+=1
		#rank
		nearest = [p2 for p2 in sorted(points, key=lambda p2: length(p1, p2))]
		if not nearest:
			break
		p1 = nearest[0]
		visited[p1.i] = i			
		
	return visited

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

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution = spiral(points, nodeCount)

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

