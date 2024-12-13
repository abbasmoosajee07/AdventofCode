"""Advent of Code - Day 22, Year 2022
Solution Started: Dec 11, 2024
Puzzle Link: https://adventofcode.com/2022/day/22
Solution by: abbasmoosajee07
Brief: [Moving in a non-square Grid, P1]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Read and sort input data into a grid
with open(D22_file_path) as file:
    input_data = file.read().split('\n\n')
    movements = re.findall(r'\d+|[RL]', input_data[1])

def build_grid(multiline_str):
    """Build a grid from the input string."""
    lines = multiline_str.split('\n')
    max_len = max(len(line) for line in lines)
    padded_lines = [list(line.ljust(max_len)) for line in lines]
    return np.array(padded_lines, dtype=str)

def find_boundaries(row):
    """Find the first and last non-space indices in a row/col."""
    indices = [i for i, char in enumerate(row) if char != ' ']
    return (indices[0], indices[-1]) if indices else (0, len(row) - 1)

def move_on_grid(grid, movement, start):
    """Execute a movement on the grid."""
    CLOCKWISE = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
    COUNTERCLOCKWISE = {'>': '^', '^': '<', '<': 'v', 'v': '>'}
    MOVE_DIRECTION = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

    row, col, direction = start
    if movement in ('L', 'R'):
        direction = CLOCKWISE[direction] if movement == 'R' else COUNTERCLOCKWISE[direction]
        return (row, col, direction)

    steps = int(movement)
    for _ in range(steps):
        dr, dc = MOVE_DIRECTION[direction]
        next_row, next_col = row + dr, col + dc

        # Handle wrapping in rows
        row_start, row_end = find_boundaries(grid[row])
        if next_col < row_start:
            next_col = row_end
        elif next_col > row_end:
            next_col = row_start

        # Handle wrapping in columns
        col_start, col_end = find_boundaries(grid[:, col])
        if next_row < col_start:
            next_row = col_end
        elif next_row > col_end:
            next_row = col_start

        # Stop if hitting a wall
        if grid[next_row, next_col] == '#':
            break

        row, col = next_row, next_col

    return (row, col, direction)

def calculate_final_password(position):
    """Calculate the final password based on the position."""
    row, col, direction = position
    direction_value = {'>': 0, 'v': 1, '<': 2, '^': 3}
    return (1000 * (row + 1)) + (4 * (col + 1)) + direction_value[direction]
def map_movement(grid, movement_list):
# Build the grid and execute movements
    start_position = (0, np.where(grid[0] == '.')[0][0], '>')
    current_position = start_position

    for movement in movement_list:
        current_position = move_on_grid(grid, movement, current_position)

    # Calculate and print the final result
    final_password = calculate_final_password(current_position)
    return final_password

grid_init = build_grid(input_data[0])
ans_p1 = map_movement(grid_init, movements)
print("Part 1:", ans_p1)
