"""Advent of Code - Day 14, Year 2023
Solution Started: Jan 2, 2025
Puzzle Link: https://adventofcode.com/2023/day/14
Solution by: abbasmoosajee07
Brief: [Tilting Platform]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()
# Load the input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

# Read and sort input data into a grid
with open(D14_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(init_grid: list) -> tuple[dict, tuple]:
    grid_dict = {}

    # Initialize boundaries with extreme values
    min_row, max_row = float('inf'), -float('inf')
    min_col, max_col = float('inf'), -float('inf')

    # Iterate through the grid to update each tile to dict and update bounds
    for row_no, row in enumerate(init_grid):
        for col_no, space in enumerate(row):
            if space != '.':
                if space not in grid_dict:
                    grid_dict[space] = set()
                grid_dict[space].add((row_no, col_no))

            # Update the boundaries
            min_row = min(min_row, row_no)
            max_row = max(max_row, row_no)
            min_col = min(min_col, col_no)
            max_col = max(max_col, col_no)

    # Define the space bounds
    grid_bounds = (min_row, max_row + 1, min_col, max_col + 1)

    return grid_dict, grid_bounds

def print_grid(grid_dict: dict, grid_bounds: tuple):
    min_row, max_row, min_col, max_col = grid_bounds
    grid_list = []

    for row_no in range(min_row, max_row):
        row = ''
        for col_no in range(min_col, max_col):
            pos = (row_no, col_no)
            found = False
            for key, positions in grid_dict.items():
                if pos in positions:
                    row += key
                    found = True
                    break
            if not found:
                row += '.'
        grid_list.append(row)

    for row in grid_list:
        print(row)

def calculate_load(grid_dict: dict) -> int:
    total_load = 0
    load_dict = {}

    # Find the maximum row index to adjust for reversed logic
    max_row = max(row for positions in grid_dict.values() for row, _ in positions)

    for positions in grid_dict.get('O', set()):
        row, _ = positions
        # Calculate the reversed row index
        reversed_row = max_row - row

        # Update the load dictionary with the reversed row index
        if (reversed_row + 1) not in load_dict:
            load_dict[reversed_row + 1] = 1
        else:
            load_dict[reversed_row + 1] += 1

    # Calculate the total load
    for row_index, count in load_dict.items():
        total_load += row_index * count

    return total_load

def tilt_platform(platform: dict, boundaries: tuple, tilt_dir: str):
    DIRECTIONS = {
        'North': (-1, 0),       # Move up
        'South': (1, 0),        # Move down
        'East': (0, 1),         # Move right
        'West': (0, -1),        # Move left
        'Northeast': (-1, 1),   # Move up and right
        'Northwest': (-1, -1),  # Move up and left
        'Southeast': (1, 1),    # Move down and right
        'Southwest': (1, -1)    # Move down and left
    }
    tilt_coords = DIRECTIONS[tilt_dir]
    dr, dc = tilt_coords
    min_row, max_row, min_col, max_col = boundaries
    fixed_blocks = set(platform.get('#', set()))
    move_blocks = set(platform.get('O', set()))
    tilted_blocks = set()
    # print('Initial Blocks Count:', len(move_blocks))

    def get_connected_blocks() -> tuple[set, tuple]:
        connected_blocks = set()
        next_row, next_col = block_row, block_col
        connected_blocks.add((next_row, next_col))
        while True:
            next_row += dr
            next_col += dc
            if (min_row <= next_row <= max_row) and (min_col <= next_col <= max_col):
                break_point = (next_row, next_col)
                if (next_row, next_col) in fixed_blocks:
                    break_point = (next_row - dr, next_col - dc)

                    break
                elif (next_row, next_col) in move_blocks:
                    connected_blocks.add((next_row, next_col))
            else:
                base_row = 0 if dr == -1 else max_row
                break_point = (base_row, next_col)
                break
        return connected_blocks, break_point

    while move_blocks:
        block_row, block_col = max(move_blocks)  # Find the "last" block based on tuple comparison
        connected, break_point = get_connected_blocks()
        final_row, final_col = break_point
        # print(connected, break_point)
        for step in range(len(connected)):
            tilt_row = (step * -dr) + final_row
            tilted_blocks.add((tilt_row, final_col))
            # print((tilt_row,final_col))
        move_blocks.difference_update(connected)  # Remove it from the set

    final_platform = {'#': fixed_blocks, 'O': tilted_blocks}
    # print('Final Block Count:', len(tilted_blocks))
    # print(tilted_blocks)
    # print_grid(final_platform, boundaries)
    return final_platform

test_input = ['O....#....', 'O.OO#....#', '.....##...', 'OO.#O....O', '.O.....O#.', 'O.#..O.#.#', '..O..#O..O', '.......O..', '#....###..', '#OO..#....']
test_score = ['OOOO.#.O..', 'OO..#....#', 'OO..O##..O', 'O..#.OO...', '........#.', '..#....#.#', '..O..#.O.O', '..O.......', '#....###..', '#....#....']

init_platform, bounds = parse_input(input_data)
# north_tilt = tilt_platform(init_platform, bounds, 'North')
# south_tilt = tilt_platform(init_platform, bounds, 'South')

tilted_platform = tilt_platform(init_platform, bounds, 'North')
load_p1 = calculate_load(tilted_platform)
print("Part 1:", load_p1)

# OOOO.#.O..
# OO..#....#
# OO..O##..O
# O..#.OO...
# ........#.
# ..#....#.#
# ..O..#.O.O
# ..O.......
# #....###..
# #....#....

SPIN_CYCLE = ['North', 'West', 'South', 'East']

# for cycle in range(1_000_000_000):
#     print(cycle)
#     tilted_platform = tilt_platform(tilted_platform, bounds, 'North')
#     load_p2 = calculate_load(tilted_platform)
# print("Part 2:", load_p2)

# After 1 cycle:
# .....#....
# ....#...O#
# ...OO##...
# .OO#......
# .....OOO#.
# .O#...O#.#
# ....O#....
# ......OOOO
# #...O###..
# #..OO#....

# After 2 cycles:
# .....#....
# ....#...O#
# .....##...
# ..O#......
# .....OOO#.
# .O#...O#.#
# ....O#...O
# .......OOO
# #..OO###..
# #.OOO#...O

# After 3 cycles:
# .....#....
# ....#...O#
# .....##...
# ..O#......
# .....OOO#.
# .O#...O#.#
# ....O#...O
# .......OOO
# #...O###.O
# #.OOO#...O

print(f"Execution Time = {time.time() - start_time:.5f}s")


