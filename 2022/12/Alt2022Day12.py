"""Advent of Code - Day 12, Year 2022
Solution Started: Dec 1, 2024
Puzzle Link: https://adventofcode.com/2022/day/12
Solution by: abbasmoosajee07
Brief: [Pathfinding on a hill]
"""

#!/usr/bin/env python3

import os, re, copy, heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read and sort input data into a grid
with open(D12_file_path) as file:
    input_data = file.read().strip().split('\n')
    letter_map = np.array([list(row) for row in input_data])


# Convert the input to a 2D list of characters
input_grid = [list(line) for line in input_data]

# Find the positions of 'S' (Start) and 'E' (End)
Start = np.array(np.where(np.array(input_grid) == "S")).flatten()
End = np.array(np.where(np.array(input_grid) == "E")).flatten()

# Initialize the number map
number_map = np.zeros_like(np.array(input_grid), dtype=int)

# Map letters to numbers (a=1, b=2, ..., z=26)
for i in range(26):
    number_map[np.array(input_grid) == chr(i + ord('a'))] = i + 1
number_map[tuple(Start)] = 1  # Start is 1
number_map[tuple(End)] = 26   # End is 26

def pathfinder_forwards(start):
    dims = number_map.shape
    distance = np.full(dims, np.inf)
    distance[tuple(start)] = 0
    unvisited = np.ones(dims)
    
    # Dijkstra's Algorithm
    priority_queue = [(0, tuple(start))]
    
    while priority_queue:
        dist, current = heapq.heappop(priority_queue)
        
        if current == tuple(End):
            return dist
        
        if unvisited[current] == 0:
            continue
        
        unvisited[current] = 0
        current_ai = np.array(current)
        adjacent_inds = [
            current_ai + [0, 1], current_ai + [1, 0], 
            current_ai - [0, 1], current_ai - [1, 0]
        ]
        adjacent_inds = [ind for ind in adjacent_inds 
                         if 0 <= ind[0] < dims[0] and 0 <= ind[1] < dims[1]]
        
        for adj in adjacent_inds:
            if number_map[tuple(adj)] < number_map[tuple(current)] + 2:
                new_dist = dist + 1
                if new_dist < distance[tuple(adj)]:
                    distance[tuple(adj)] = new_dist
                    heapq.heappush(priority_queue, (new_dist, tuple(adj)))
    
    return distance[tuple(End)]


def pathfinder_backwards(end):
    dims = number_map.shape
    distance = np.full(dims, np.inf)
    distance[tuple(end)] = 0
    unvisited = np.ones(dims)
    
    # Dijkstra's Algorithm
    priority_queue = [(0, tuple(end))]
    
    while priority_queue:
        dist, current = heapq.heappop(priority_queue)
        
        if np.all(unvisited == 0):
            break
        
        if unvisited[current] == 0:
            continue
        
        unvisited[current] = 0
        current_ai = np.array(current)
        adjacent_inds = [
            current_ai + [0, 1], current_ai + [1, 0], 
            current_ai - [0, 1], current_ai - [1, 0]
        ]
        adjacent_inds = [ind for ind in adjacent_inds 
                         if 0 <= ind[0] < dims[0] and 0 <= ind[1] < dims[1]]
        
        for adj in adjacent_inds:
            if number_map[tuple(adj)] > number_map[tuple(current)] - 2:
                new_dist = dist + 1
                if new_dist < distance[tuple(adj)]:
                    distance[tuple(adj)] = new_dist
                    heapq.heappush(priority_queue, (new_dist, tuple(adj)))
    
    lowest_points = np.array(np.where(number_map == 1)).T
    return np.min([distance[tuple(point)] for point in lowest_points])

# Print the results
print(pathfinder_forwards(Start))
print(pathfinder_backwards(End))
