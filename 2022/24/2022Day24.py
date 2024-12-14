"""Advent of Code - Day 24, Year 2022
Solution Started: Dec 13, 2024
Puzzle Link: https://adventofcode.com/2022/day/24
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
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
    BLIZZARD_MOVEMENT = {'>': (0, 1), '<':(0, -1),
                        'v':(1, 0),  '^':(-1, 0)}
    wrap_around = {
        '>': lambda r, c: (r, 1),  # Wrap to the first column
        '<': lambda r, c: (r, total_cols - 1),  # Wrap to the last column
        'v': lambda r, c: (1, c),  # Wrap to the first row
        '^': lambda r, c: (total_rows - 1, c)  # Wrap to the last row
    }
    total_rows, total_cols = len(map), len(map[0])
    next_map = copy.deepcopy(map)
    for row_no, row in enumerate(map):
        for col_no, all_blizzards in enumerate(row):
            pos = (row_no, col_no)
            blizzard_list = list(all_blizzards)
            for point in blizzard_list:
                if point in ['>','<','v','^']:
                    dr, dc = BLIZZARD_MOVEMENT[point]
                    new_row = row_no + dr
                    new_col = col_no + dc
                    new_pos = (new_row, new_col)
                    next_old = map[new_pos]
                    # Handle wrap-around logic if hitting a wall
                    if next_old == '#':
                        if point in wrap_around:
                            new_row, new_col = wrap_around[point](row_no, col_no)
                            new_pos = (new_row, new_col)
                            next_old = map[new_pos]

                    next_point = next_map[new_pos]
                    original_point = next_map[pos]
                    if next_point == '.':
                        next_map[new_pos] = point
                    else:
                        next_point += point
                        next_map[new_pos] = next_point
                    if len(original_point) == 1:
                        next_map[pos] = '.'
                    else:
                        next_map[pos] = original_point
                    #show_map(next_map)
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

init_map = example_1
new_map = init_map
show_map(new_map)
for minute in range(1,6):
    print(f"{minute=}")
    new_map = track_blizzards(new_map)
    show_map(new_map)
print(new_map)
