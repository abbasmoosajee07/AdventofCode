"""Advent of Code - Day 12, Year 2024
Solution Started: Dec 12, 2024
Puzzle Link: https://adventofcode.com/2024/day/12
Solution by: abbasmoosajee07
Brief: [Fencing and Gardens]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

# Load the input data from the specified file path
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read and sort input data into a grid
with open(D12_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_map = [list(row) for row in input_data]


def get_region_plants(grid, pos, visited_global):
    """Calculate area, total perimeter, and bulk fence perimeter for a given region."""
    rows, cols = len(grid), len(grid[0])
    target_value = grid[pos[0]][pos[1]]

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    visited_local = set()
    queue = deque([pos])
    area = 0
    perimeter = 0
    perimeter_map = {}

    while queue:
        cur_row, cur_col = queue.popleft()
        if (cur_row, cur_col) in visited_local or (cur_row, cur_col) in visited_global:
            continue
        visited_local.add((cur_row, cur_col))
        visited_global.add((cur_row, cur_col))
        area += 1

        for dr, dc in DIRECTIONS:
            new_row, new_col = cur_row + dr, cur_col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row][new_col] == target_value:
                    if (new_row, new_col) not in visited_local:
                        queue.append((new_row, new_col))
                else:
                    perimeter += 1
                    if (dr, dc) not in perimeter_map:
                        perimeter_map[(dr, dc)] = set()
                    perimeter_map[(dr, dc)].add((cur_row, cur_col))
            else:
                perimeter += 1
                if (dr, dc) not in perimeter_map:
                    perimeter_map[(dr, dc)] = set()
                perimeter_map[(dr, dc)].add((cur_row, cur_col))

    sides = 0
    for direction, positions in perimeter_map.items():
        seen_sides = set()
        for pos in positions:
            if pos not in seen_sides:
                sides += 1
                queue = deque([pos])
                while queue:
                    r, c = queue.popleft()
                    if (r, c) in seen_sides:
                        continue
                    seen_sides.add((r, c))
                    for dr, dc in DIRECTIONS:
                        nr, nc = r + dr, c + dc
                        if (nr, nc) in positions:
                            queue.append((nr, nc))

    return visited_local, area, perimeter, sides

def calc_fence_price(grid):
    """Calculate the total and bulk fence prices for all regions in the grid."""
    visited_global = set()
    total_price = 0
    bulk_price = 0

    for row_no, row in enumerate(grid):
        for col_no, plant in enumerate(row):
            pos = (row_no, col_no)
            if pos not in visited_global:
                region, area, total_fence, bulk_fence = get_region_plants(grid, pos, visited_global)
                total_price += (total_fence * area)
                bulk_price += (bulk_fence * area)
                # print(f"{plant}, area={area}, total_fence={total_fence}, bulk_fence={bulk_fence}")

    return total_price, bulk_price

total_price, bulk_price = calc_fence_price(input_data)
print("Part 1:", total_price)
print("Part 2:", bulk_price)
