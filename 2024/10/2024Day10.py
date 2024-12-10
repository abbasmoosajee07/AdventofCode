"""Advent of Code - Day 10, Year 2024
Solution Started: Dec 10, 2024
Puzzle Link: https://adventofcode.com/2024/day/10
Solution by: abbasmoosajee07
Brief: [Hiking Trails]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read and sort input data into a grid
with open(D10_file_path) as file:
    input_data = file.read().strip().split('\n')
    map_grid = np.array([[int(num) for num in list(row)] for row in input_data])

def find_all_zeros(grid):
    zeros_positions = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                zeros_positions.append((row, col))
    return zeros_positions

def find_trails(grid, start):
    rows, cols = len(grid), len(grid[0])  # Dimensions of the grid
    visited = set()  # Track visited cells
    queue = deque([start])  # Initialize the queue with the start cell
    visited.add(start)  # Mark the start cell as visited
    
    # Directions for neighbors (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    result = []  # To store all reachable cells with value 9
    
    while queue:
        current = queue.popleft()  # Dequeue the front cell
        row, col = current
        pos_height = grid[row][col]  # Height of the current position
        
        # If the current cell has value 9, add it to the result
        if pos_height == 9:
            result.append(current)
        
        # Check all 4 possible neighbors
        for dr, dc in directions:
            r, c = row + dr, col + dc
            
            if 0 <= r < rows and 0 <= c < cols and (r, c) not in visited:
                next_height = grid[r][c]
                diff_height = (next_height - pos_height)
                
                # Move to the neighbor if the height difference constraint is satisfied
                if diff_height == 1:
                    visited.add((r, c))  # Mark neighbor as visited
                    queue.append((r, c))  # Add neighbor to the queue
    
    return result

def find_distinct_trails(grid, start):
    rows, cols = len(grid), len(grid[0])  # Dimensions of the grid
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Neighbor directions (up, down, left, right)
    
    # Queue to store current paths; each item is a path (list of cells)
    queue = deque([[start]])
    distinct_trails = []  # List to store all distinct trails

    while queue:
        current_path = queue.popleft()  # Dequeue the current trail
        current_cell = current_path[-1]  # Get the last cell in the current path
        row, col = current_cell
        pos_height = grid[row][col]  # Height of the current position

        # If the last cell in the trail has value 9, store this trail
        if pos_height == 9:
            distinct_trails.append(current_path)
        
        # Explore neighbors to extend the trail
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:  # Check bounds
                next_height = grid[r][c]
                diff_height = next_height - pos_height

                # Move to the neighbor if the height difference constraint is satisfied
                if diff_height == 1:
                    # Prevent revisiting the same cell within the same path
                    if (r, c) not in current_path:
                        # Extend the current path
                        new_path = current_path + [(r, c)]
                        queue.append(new_path)

    return distinct_trails

all_trails_p1 = 0
all_trails_p2 = 0
all_start = find_all_zeros(map_grid)
for start_pos in all_start:
    trails_p1 = find_trails(map_grid, start_pos)
    all_trails_p1 += len(trails_p1)
    trails_p2 = find_distinct_trails(map_grid, start_pos)
    all_trails_p2 += len(trails_p2)

print("Part 1:", all_trails_p1)
print("Part 2:", all_trails_p2)
