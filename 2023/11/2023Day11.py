"""Advent of Code - Day 11, Year 2023
Solution Started: Dec 28, 2024
Puzzle Link: https://adventofcode.com/2023/day/11
Solution by: abbasmoosajee07
Brief: [Expanding Galaxies]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path) as file:
    input_data = file.read().strip().split('\n')

def galaxy_coordinates(space_grid: list[str]) -> dict:
    galaxy_no = 0
    galaxy_dict = {}

    # Initialize boundaries with extreme values
    min_row, max_row = float('inf'), -float('inf')
    min_col, max_col = float('inf'), -float('inf')

    # Iterate through the grid to find galaxies and update bounds
    for row_no, row in enumerate(space_grid):
        for col_no, space in enumerate(row):
            if space == '#':
                galaxy_no += 1
                galaxy_dict[(row_no, col_no)] = galaxy_no

                # Update the boundaries
                min_row = min(min_row, row_no)
                max_row = max(max_row, row_no)
                min_col = min(min_col, col_no)
                max_col = max(max_col, col_no)

    # Define the space bounds
    space_bounds = (min_row, max_row + 1, min_col, max_col + 1)

    return galaxy_dict, space_bounds

def expand_galaxies(galaxy_dict: dict, boundaries: tuple, expansion_shift: int = 1) -> dict:
    min_row, max_row, min_col, max_col = boundaries

    # Determine unused rows and columns
    unused_rows = set(range(min_row, max_row)) - {row for row, _ in galaxy_dict.keys()}
    unused_cols = set(range(min_col, max_col)) - {col for _, col in galaxy_dict.keys()}

    expanded_galaxies = {}
    for (original_row, original_col), galaxy_id in galaxy_dict.items():
        # Find rows and columns before the current galaxy that are unused
        unused_rows_before = set(range(min_row, original_row)) & unused_rows
        unused_cols_before = set(range(min_col, original_col)) & unused_cols

        # Calculate the updated position
        shifted_row = original_row + len(unused_rows_before) * (expansion_shift - 1)
        shifted_col = original_col + len(unused_cols_before) * (expansion_shift - 1)

        # Store the expanded galaxy position
        expanded_galaxies[(shifted_row, shifted_col)] = galaxy_id

    return expanded_galaxies

def all_galaxy_paths(galaxy_dict: dict) -> int:
    path_sum = 0
    galaxy_coords = list(galaxy_dict.keys())

    # Iterate over all unique pairs of galaxies
    for i, coords_1 in enumerate(galaxy_coords):
        for coords_2 in galaxy_coords[i + 1:]:
            # Calculate the Manhattan distance
            bfs_path = abs(coords_1[0] - coords_2[0]) + \
                        abs(coords_1[1] - coords_2[1])
            path_sum += bfs_path

    return path_sum

init_galaxies, bounds = galaxy_coordinates(input_data)

# Part 1: Expansion with shift of 2
galaxy_positions_p1 = expand_galaxies(init_galaxies, bounds, expansion_shift=2)
galaxy_paths_p1 = all_galaxy_paths(galaxy_positions_p1)
print("Part 1:", galaxy_paths_p1)

# Part 2: Expansion with a large shift
galaxy_positions_p2 = expand_galaxies(init_galaxies, bounds, expansion_shift=1_000_000)
galaxy_paths_p2 = all_galaxy_paths(galaxy_positions_p2)
print("Part 2:", galaxy_paths_p2)

