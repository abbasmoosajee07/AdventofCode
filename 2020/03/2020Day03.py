# Advent of Code - Day 3, Year 2020
# Solution Started: Nov 19, 2024
# Puzzle Link: https://adventofcode.com/2020/day/3
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

# Load the input data from the specified file path
D03_file = "Day03_input.txt"
D03_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D03_file)

# Read and sort input data into a grid
with open(D03_file_path) as file:
    input_data = file.read().strip().split('\n')

def create_full_map(initial_map, copy):
    full_map = []
    for row in initial_map:
        new_row = list(row) * copy
        full_map.append(new_row)
    return np.array(full_map)

def count_trees(grid, start, right, down):
    rows, cols = len(grid), len(grid[0])  # Dimensions of the grid
    x, y = start  # Start from the initial position
    tree_count = 0
    
    while x < rows:  # Stop if we reach the last row
        # Check if the current position contains a tree
        if grid[x][y % cols] == '#':  # Handle horizontal wrapping
            tree_count += 1
        
        # Move according to the specified right/down steps
        x += down
        y += right  # Wrap horizontally by using y % cols

    return tree_count


# Create a replicated map and run the function
replicated_map = create_full_map(input_data, len(input_data))

# Starting position
start_pos = (0, 0)

# Right 3, Down 1 (the movement pattern for Day 3, Part 1)
ans_p1 = count_trees(replicated_map, start_pos, 3, 1)

print(f"Part 1: {ans_p1}")

# Right 1, down 1.
trees_r1d1 = count_trees(replicated_map, start_pos, 1, 1)
# Right 3, down 1.
trees_r3d1 = count_trees(replicated_map, start_pos, 3, 1)
# Right 5, down 1.
trees_r5d1 = count_trees(replicated_map, start_pos, 5, 1)
# Right 7, down 1.
trees_r7d1 = count_trees(replicated_map, start_pos, 7, 1)
# Right 1, down 2.
trees_r1d2 = count_trees(replicated_map, start_pos, 1, 2)

ans_p2 = trees_r1d1 * trees_r3d1 * trees_r5d1 * trees_r7d1 * trees_r1d2
print(f"Part 2: {ans_p2}")
