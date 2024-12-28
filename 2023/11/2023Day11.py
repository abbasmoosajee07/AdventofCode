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

def print_space(expanded_space: list, galaxies: dict):
    expanded_grid = []
    for row_no, row in enumerate(expanded_space):
        empty_row = []
        for col_no, space in enumerate(row):
            if (row_no, col_no) in galaxies.keys():
                galaxy_no = str(galaxies[(row_no, col_no)]).zfill(3)
                empty_row.append(galaxy_no)
            else:
                empty_row.append(' ' + space + ' ')
        expanded_grid.append(empty_row)

    for row in expanded_grid:
        print(''.join(row))

def expand_galaxies(init_grid: list[str]) -> list[str]:
    def expand_space(grid: list[str]) -> list[str]:
        """Expand the grid by inserting rows or columns of empty space ('.')."""
        expanded_grid = []
        for row in grid:
            expanded_grid.append(row)
            if row.count('.') == len(row):
                expansion = [row] * 1  # Add a million rows of empty space
                expanded_grid.extend(expansion)
        return expanded_grid

    # Step 1: Expand rows
    grid_with_extra_rows = expand_space(init_grid)

    # Step 2: Expand columns by transposing, expanding, and transposing back
    transposed_grid = np.transpose([list(row) for row in grid_with_extra_rows])
    transposed_as_strings = [''.join(row) for row in transposed_grid]
    grid_with_extra_cols = expand_space(transposed_as_strings)

    # Convert back to the original orientation
    final_transposed_grid = np.transpose([list(row) for row in grid_with_extra_cols])
    final_expanded_grid = [''.join(row) for row in final_transposed_grid]

    return final_expanded_grid

def galaxy_coordinates(space_grid: list[str]) -> dict:
    galaxy_dict = {}
    galaxy_no = 0
    for row_no, row in enumerate(space_grid):
        for col_no, space in enumerate(row):
            if space == '#':
                galaxy_no += 1
                galaxy_dict[(row_no, col_no)] = galaxy_no
    return galaxy_dict

def pair_galaxies(galaxy_dict: dict) -> int:
    total_pairs = 0
    galaxy_pairs = set()
    all_path = 0

    for coords_1 in galaxy_dict.keys():
        for coords_2 in galaxy_dict.keys():
            if coords_1 != coords_2:
                # Ensure the pair is added in a consistent order
                pair = tuple(sorted((coords_1, coords_2)))
                if pair not in galaxy_pairs:
                    total_pairs += 1
                    galaxy_pairs.add(pair)
                    bfs_path = abs(coords_1[0]-coords_2[0]) + abs(coords_1[1]-coords_2[1])
                    all_path += bfs_path

    return all_path

test_input = ['...#......', '.......#..', '#.........', '..........', '......#...', '.#........', '.........#', '..........', '.......#..', '#...#.....']
expanded_grid = expand_galaxies(input_data)
galaxies = galaxy_coordinates(expanded_grid)
all_galaxy_paths = pair_galaxies(galaxies)
print("Part 1:", all_galaxy_paths)
# print_space(expanded_grid, galaxies)


