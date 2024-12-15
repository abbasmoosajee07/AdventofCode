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

# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read and sort input data into a grid
with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_map  = np.array([list(row) for row in input_data], dtype=object)

def show_map(map):
    for row in map:
        print_row = ''
        for cell in row:
            if len(cell) == 1:
                print_row += cell[0]
            else:
                print_row += str(len(cell))
        print(print_row)

DIRECTIONS =[(-1, 0), (1, 0), (0, -1), (0, 1)] # N, S, W, E


def track_blizzards(map):
    BLIZZARD_MOVEMENT = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}
    
    # Wrap-around logic for blizzards
    def wrap_around(direction, r, c):
        if direction == '>':  # Wrap to the first column
            return (r, 1)
        elif direction == '<':  # Wrap to the last column
            return (r, len(map[0]) - 2)
        elif direction == 'v':  # Wrap to the first row
            return (1, c)
        elif direction == '^':  # Wrap to the last row
            return (len(map) - 2, c)

    total_rows, total_cols = len(map), len(map[0])
    next_map = [['.' for _ in range(total_cols)] for _ in range(total_rows)]
    
    # Copy walls ('#') from the original map to the new map
    for r in range(total_rows):
        for c in range(total_cols):
            if map[r][c] == '#':
                next_map[r][c] = '#'
    
    for row_no, row in enumerate(map):
        for col_no, cell in enumerate(row):
            if cell not in ['#', '.']:  # Cell contains blizzards
                for point in cell:  # Handle multiple blizzards in one cell
                    dr, dc = BLIZZARD_MOVEMENT[point]
                    new_row, new_col = row_no + dr, col_no + dc

                    # Handle wrap-around
                    if map[new_row][new_col] == '#':
                        new_row, new_col = wrap_around(point, row_no, col_no)

                    # Move blizzard to the new position
                    if next_map[new_row][new_col] in ['.', '#']:
                        next_map[new_row][new_col] = point
                    else:
                        next_map[new_row][new_col] += point

    return next_map

example_1 = np.array([
    ['#', '.', '#', '#', '#', '#', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '>', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', 'v', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '#', '#', '#', '#', '.', '#']
], dtype=object)

example_2 = np.array([
    ['#', '.', '#', '#', '#', '#', '#', '#'],
    ['#', '>', '>', '.', '<', '^', '<', '#'],
    ['#', '.', '<', '.', '.', '<', '<', '#'],
    ['#', '>', 'v', '.', '>', '<', '>', '#'],
    ['#', '<', '^', 'v', '^', '^', '>', '#'],
    ['#', '#', '#', '#', '#', '#', '.', '#']
], dtype=object)

init_map = example_2
new_map = init_map
show_map(new_map)
for minute in range(1,19):
    print(f"{minute=}")
    new_map = track_blizzards(new_map)
    show_map(new_map)

# print(new_map)
