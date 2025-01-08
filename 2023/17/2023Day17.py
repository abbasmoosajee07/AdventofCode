"""Advent of Code - Day 17, Year 2023
Solution Started: Jan 7, 2025
Puzzle Link: https://adventofcode.com/2023/day/17
Solution by: abbasmoosajee07
Brief: [Weighted Pathfinding]
"""

#!/usr/bin/env python3

import os, re, copy, time, heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from heapq import heappop, heappush
start_time = time.time()

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_grid(init_grid: list) -> tuple[dict, tuple]:
    grid_dict = {}

    # Initialize boundaries with extreme values
    min_row, max_row = float('inf'), -float('inf')
    min_col, max_col = float('inf'), -float('inf')

    # Iterate through the grid to update each tile to dict and update bounds
    for row_no, row in enumerate(init_grid):
        for col_no, tile in enumerate(row):
            grid_dict[(row_no, col_no)] = int(tile)

            # Update the boundaries
            min_row = min(min_row, row_no)
            max_row = max(max_row, row_no)
            min_col = min(min_col, col_no)
            max_col = max(max_col, col_no)

    # Define the space bounds
    grid_bounds = (min_row, max_row + 1, min_col, max_col + 1)

    return grid_dict, grid_bounds

def find_heat_loss(grid_dict: dict, grid_bounds: tuple, crucible_len: tuple) -> int:
    MIN_ROW, MAX_ROW, MIN_COL, MAX_COL = grid_bounds
    min_len, max_len = crucible_len
    DIRECTIONS = {(-1, 0):'^', (1, 0):'v', (0, -1):'<', (0, 1):'>'}

    # tuple: (heat-loss, x-coord, y-coord, length-of-current-run, x-direction, y-direction)
    queue = [(0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 1, 0)]
    visited = set()

    while queue:
        loss, row, col, k, dr, dc = heappop(queue)
        if row == MAX_ROW - 1 and col == MAX_COL - 1:
            if k < min_len:
                continue
            break

        if (row, col, k, dr, dc) in visited:
            continue

        visited.add((row, col, k, dr, dc))

        for new_dr, new_dc in DIRECTIONS.keys():
            straight = (new_dr == dr and new_dc == dc)
            new_row, new_col = row + new_dr, col + new_dc

            if any((new_dr == -dr and new_dc == -dc,
                    k == max_len and straight,
                    k <  min_len and not straight,
                    new_row < 0, new_col < 0,
                    new_row == MAX_ROW, new_col == MAX_COL)):
                continue

            new_k = k + 1 if straight else 1
            heappush(queue, (loss + grid_dict[(new_row,new_col)], new_row, new_col, new_k, new_dr, new_dc))

    return loss

grid_dict, bounds = parse_grid(input_data)
min_heat_p1 = find_heat_loss(grid_dict, bounds, (1, 3))
print("Part 1:", min_heat_p1)

min_heat_p2 = find_heat_loss(grid_dict, bounds, (4, 10))
print("Part 2:", min_heat_p2)
print(f"Execution Time = {time.time() - start_time:.5f}s")
