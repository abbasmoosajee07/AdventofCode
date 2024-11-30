"""Advent of Code - Day 8, Year 2022
Solution Started: Nov 29, 2024
Puzzle Link: https://adventofcode.com/2022/day/8
Solution by: abbasmoosajee07
Brief: [Tree Visibility]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D08_file = "Day08_input.txt"
D08_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D08_file)

# Read and sort input data into a grid
with open(D08_file_path) as file:
    input_data = file.read().strip().split('\n')
    tree_grid = np.array([[int(num) for num in list(row)] for row in input_data])
def visibility_from_edge(pos, grid):

    # Define directions: (row_offset, col_offset)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    visible_count = 0
    row, col  = pos
    neighbors = []
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        # Check bounds
        current_tree = grid[pos]
        if 0 <= new_row < num_rows and 0 <= new_col < num_cols :
            neighbors.append((new_row, new_col))
            if (dr, dc) == (-1, 0): # upwards
                adjacent_trees = grid[0:new_row+1, new_col]
            if (dr, dc) == (+1, 0): # downwards
                adjacent_trees = grid[new_row:, new_col]
            if (dr, dc) == (0, +1): # towards right
                adjacent_trees = grid[new_row, new_col:]
            if (dr, dc) == (0, -1): # towards left
                adjacent_trees = grid[new_row, :new_col+1]
            tree_set = set(adjacent_trees)
            if all(current_tree > tree for tree in tree_set):
                visible_count += 1
    return visible_count

all_visible_trees = 0

for x in range(1,len(tree_grid)-1):
    for y in range(1,len(tree_grid[0])-1):
        visibility = visibility_from_edge((x, y), tree_grid)
        if visibility >= 1:
            all_visible_trees += 1
all_visible_trees += (4 * len(tree_grid)) - 4
print("Part 1:", all_visible_trees)

def visibility_from_tree(pos, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    row, col = pos
    current_tree = grid[row][col]
    num_rows = len(grid)
    num_cols = len(grid[0])

    tree_score = []  # Stores visibility distances in all directions

    for dr, dc in directions:
        visible_count = 0
        new_row, new_col = row + dr, col + dc

        # Traverse in the current direction until out of bounds or blocked
        while 0 <= new_row < num_rows and 0 <= new_col < num_cols:
            visible_count += 1  # Count this tree
            if grid[new_row][new_col] >= current_tree:
                break  # Stop if a taller or equal tree blocks the view
            new_row += dr
            new_col += dc

        tree_score.append(visible_count)

    # Return the product of visibility distances in all directions
    return np.prod(tree_score)

scenic_score = 0

for x in range(1,len(tree_grid)-1):
    for y in range(1,len(tree_grid[0])-1):
        visibility = visibility_from_tree((x, y), tree_grid)
        scenic_score = max(scenic_score, visibility)
print("Part 2:", scenic_score)