# Advent of Code - Day 15, Year 2021
# Solution Started: Nov 24, 2024
# Puzzle Link: https://adventofcode.com/2021/day/15
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy, heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and parse the input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split('\n')

# Parse the input grid
grid = [
    [int(c) for c in row]
    for row in input_data
]

# Function to expand the grid horizontally and vertically
def expand_grid(grid, times):
    original_rows, original_cols = len(grid), len(grid[0])
    expanded_rows, expanded_cols = original_rows * times, original_cols * times
    expanded_grid = [[0] * expanded_cols for _ in range(expanded_rows)]
    
    for i in range(expanded_rows):
        for j in range(expanded_cols):
            # Calculate the value based on the original grid
            original_value = grid[i % original_rows][j % original_cols]
            increment = (i // original_rows) + (j // original_cols)
            expanded_grid[i][j] = (original_value + increment - 1) % 9 + 1  # Wrap around at 9
    
    return expanded_grid

# Function to find the lowest-cost path
def find_lowest_path(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    # Priority queue: (cumulative_cost, row, col)
    pq = [(0, 0, 0)]  # Start with top-left corner with a cost of 0
    visited = set()  # To track visited nodes
    
    while pq:
        cost, r, c = heapq.heappop(pq)
        
        # If we reach the bottom-right corner, return the cost
        if (r, c) == (rows - 1, cols - 1):
            return cost
        
        # Skip if already visited
        if (r, c) in visited:
            continue
        visited.add((r, c))
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                heapq.heappush(pq, (cost + grid[nr][nc], nr, nc))

# Expand the grid
expanded_grid = expand_grid(grid, times=5)

# Find and print the lowest path cost for the original grid
print("Part 1: (Original Grid)", find_lowest_path(grid))

# Find and print the lowest path cost for the expanded grid
print("Path 2: (Expanded Grid)", find_lowest_path(expanded_grid))
