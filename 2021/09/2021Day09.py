# Advent of Code - Day 9, Year 2021
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2021/day/9
# Solution by: [abbasmoosajee07]
# Brief: [Sea Levels and Maps]

#!/usr/bin/env python3

import os, re, copy, heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D09_file = "Day09_input.txt"
D09_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D09_file)

# Read and sort input data into a grid
with open(D09_file_path) as file:
    input_data = file.read().strip().split('\n')
    num_list = [[int(num) for num in list(row)]
                    for row in input_data ]
    level_map = np.array(num_list)

def calculate_risk_level(grid, pos):
    row, col = pos
    total_rows, total_cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    neighbors = []
    adjacent_level = []
    pos_level = grid[pos]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < total_rows and 0 <= c < total_cols:  # Check boundaries
            neighbors.append((r, c))
            neighbor_level = grid[(r,c)]
            if pos_level < neighbor_level:
                adjacent_level.append(neighbor_level)
    if len(adjacent_level) == len(neighbors):
        return pos_level
    else:
        return None

def calculate_total_risk(grid):
    total_risk = 0
    low_points = []
    for row_no, row in enumerate(grid):
        for col_no, col in enumerate(row):
            pos = (row_no, col_no)
            risk_level = calculate_risk_level(grid, pos)
            if risk_level is not None:
                total_risk += (risk_level + 1)
                low_points.append(pos)
    return total_risk, low_points

ans_p1, lowest_points = calculate_total_risk(level_map)
print("Part 1:", ans_p1)

def find_basin_size(grid, start):
    """Find the size of a basin starting from the given position."""
    total_rows, total_cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    visited = set()
    stack = [start]
    basin_size = 0

    while stack:
        row, col = stack.pop()
        if (row, col) in visited:
            continue
        visited.add((row, col))

        # Add the current position to the basin if it's less than 9
        if grid[row][col] < 9:
            basin_size += 1
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < total_rows and 0 <= c < total_cols:
                    stack.append((r, c))
    
    return basin_size

def find_low_points(grid):
    """Find all low points in the grid."""
    total_rows, total_cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    low_points = []

    for row in range(total_rows):
        for col in range(total_cols):
            is_low_point = True
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < total_rows and 0 <= c < total_cols and grid[r][c] <= grid[row][col]:
                    is_low_point = False
                    break
            if is_low_point:
                low_points.append((row, col))
    
    return low_points

def largest_basins(grid):
    # Find all low points
    low_points = find_low_points(grid)

    # Calculate the basin size for each low point
    basin_sizes = [find_basin_size(grid, pos) for pos in low_points]

    # Find the three largest basins
    three_big_basins = heapq.nlargest(3, basin_sizes)

    # Return the product of the three largest basins
    return np.prod(three_big_basins)

# Compute the result for Part 2
ans_p2 = largest_basins(level_map)
print("Part 2:", ans_p2)  # Output should match the expected result for the example
