"""Advent of Code - Day 24, Year 2022
Solution Started: Dec 13, 2024
Puzzle Link: https://adventofcode.com/2022/day/24
Solution by: abbasmoosajee07
Brief: [Moving in a Blizzard]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read and sort input data into a grid
with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n')

def initialise_map(input_data):
    grid_map  = np.array([list(row) for row in input_data], dtype=object)
    total_rows, total_cols = len(grid_map), len(grid_map[0])
    empty_map = [['.' for _ in range(total_cols)] for _ in range(total_rows)]
    non_wall_cells = []

    # Assuming start and end is on the border
    for row_index, row in enumerate(grid_map):
        for col_index, cell in enumerate(row):
            if cell == '.':
                non_wall_cells.append((row_index, col_index))
            if grid_map[row_index][col_index] in ['#','S','T','E']:
                empty_map[row_index][col_index] = grid_map[row_index][col_index]

    # Define the start and target cells
    start, target = non_wall_cells[0], non_wall_cells[-1]

    # Mark start and target cells in both maps
    grid_map[start] = 'S'
    grid_map[target] = 'T'
    empty_map[start[0]][start[1]] = 'S'
    empty_map[target[0]][target[1]] = 'T'
    return empty_map, grid_map, start, target

#!/usr/bin/env python3

import os
import numpy as np
from collections import deque

# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read the input data from file
with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n')

def show_map(map, pos=(0, 0)):
    """
    Display the map, marking the current position with 'E'.
    """
    map[pos[0]][pos[1]] = 'E'
    for row in map:
        print_row = ''.join(str(len(cell)) if isinstance(cell, list) else cell for cell in row)
        print(print_row)

def initialise_map(input_data):
    """
    Initialize the map from the input data and find the start and target positions.
    """
    grid_map = np.array([list(row) for row in input_data], dtype=object)
    total_rows, total_cols = len(grid_map), len(grid_map[0])
    
    # Create an empty map with '.' representing empty spaces
    non_wall_cells = []
    
    # Identify non-wall cells and store their coordinates
    for row_index, row in enumerate(grid_map):
        for col_index, cell in enumerate(row):
            if cell == '.':
                non_wall_cells.append((row_index, col_index))

    # Define the start and target positions
    start, target = non_wall_cells[0], non_wall_cells[-1]

    # Mark the start and target positions on both the grid_map and empty_map
    grid_map[start] = 'S'
    grid_map[target] = 'T'
    
    return grid_map, start, target

def calculate_bad_cells(grid_map, rows, cols):
    """
    Calculate the 'bad' cells where blizzards are present for each time step.
    """
    BAD_CELLS = {}
    
    # Precompute bad cells at each time step
    for storm in range((rows - 2) * (cols - 2) + 1):
        BAD = set()
        for r in range(rows):
            for c in range(cols):
                if grid_map[r][c] == '>':
                    BAD.add((r, 1 + ((c - 1 + storm) % (cols - 2))))  # Move right
                elif grid_map[r][c] == 'v':
                    BAD.add((1 + ((r - 1 + storm) % (rows - 2)), c))  # Move down
                elif grid_map[r][c] == '<':
                    BAD.add((r, 1 + ((c - 1 - storm) % (cols - 2))))  # Move left
                elif grid_map[r][c] == '^':
                    BAD.add((1 + ((r - 1 - storm) % (rows - 2)), c))  # Move up
        BAD_CELLS[storm] = BAD
    
    return BAD_CELLS

def bfs_to_target(grid_map, start, rows, cols):
    """
    Perform BFS to find the shortest path to the target while avoiding blizzards.
    """
    # Get the precomputed bad cells for each time step
    BAD_CELLS = calculate_bad_cells(grid_map, rows, cols)
    
    # Initialize the BFS queue and seen states
    p1 = False
    SEEN = set()
    start_state = (start[0], start[1], 0, False, False)  # (r, c, time, reached_end, reached_start)
    Q = deque([start_state])
    
    while Q:
        r, c, storm, got_end, got_start = Q.popleft()

        # Skip invalid positions (walls or out of bounds)
        if not (0 <= r < rows and 0 <= c < cols and grid_map[r][c] != '#'):
            continue
        
        # If reached the target row (end)
        if r == rows - 1 and got_end and got_start:
            print("Part 2:", storm)
            break
        
        # Handle reaching the target row for Part 1
        if r == rows - 1 and not p1:
            print("Part 1:", storm)
            p1 = True
        
        # Update flags based on position
        if r == rows - 1:
            got_end = True
        if r == 0 and got_end:
            got_start = True
        
        # Skip if this state has already been seen (avoid revisiting)
        if (r, c, storm, got_start, got_end) in SEEN:
            continue
        SEEN.add((r, c, storm, got_start, got_end))
        
        # Get the 'bad' cells for the next time step
        BAD = BAD_CELLS[storm + 1]

        # Explore the current position and adjacent cells
        if (r, c) not in BAD:
            Q.append((r, c, storm + 1, got_end, got_start))  # Stay in place
        if (r + 1, c) not in BAD:
            Q.append((r + 1, c, storm + 1, got_end, got_start))  # Move down
        if (r - 1, c) not in BAD:
            Q.append((r - 1, c, storm + 1, got_end, got_start))  # Move up
        if (r, c + 1) not in BAD:
            Q.append((r, c + 1, storm + 1, got_end, got_start))  # Move right
        if (r, c - 1) not in BAD:
            Q.append((r, c - 1, storm + 1, got_end, got_start))  # Move left

# Initialize the map and start BFS
grid_map, start, target = initialise_map(input_data)
rows, cols = len(grid_map), len(grid_map[0])
bfs_to_target(grid_map, start, rows, cols)