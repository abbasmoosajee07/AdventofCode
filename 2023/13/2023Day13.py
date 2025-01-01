"""Advent of Code - Day 13, Year 2023
Solution Started: Jan 1, 2025
Puzzle Link: https://adventofcode.com/2023/day/13
Solution by: abbasmoosajee07
Brief: [Checking Reflections]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

# Read and sort input data into a grid
with open(D13_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def check_reflection(init_pattern: list) -> int:
    """
    Find the reflection point in a given 2D pattern.

    Parameters:
        init_pattern (list): A 2D list representing the initial pattern.

    Returns:
        int: The reflection point row number, or 0 if no reflection is found.
    """
    reflection_point = 0

    # Transpose the grid for easier row comparisons
    transposed_pattern = np.transpose(init_pattern)
    pattern_length = len(transposed_pattern)

    for row_no in range(pattern_length - 1):
        current_row = transposed_pattern[row_no]
        next_row = transposed_pattern[row_no + 1]

        # Check if the current row and the next row are identical
        if np.array_equal(current_row, next_row):
            reflection_length = pattern_length - (row_no + 1)

            # Calculate slice indices for the base and reflected patterns
            base_start = max(0, (row_no + 1) - reflection_length)
            base_end = row_no + 1
            reflected_start = row_no + 1
            reflected_end = reflected_start + (base_end - base_start)

            # Define the base and reflected patterns
            base_pattern = transposed_pattern[base_start:base_end]
            reflected_pattern = transposed_pattern[reflected_start:reflected_end]

            # Check if the base pattern matches the reflected pattern
            if np.array_equal(base_pattern, reflected_pattern[::-1]):
                reflection_point = reflected_start
                break

    return reflection_point

test_input_1 = ['#.##..##.\n..#.##.#.\n##......#\n##......#\n..#.##.#.\n..##..##.\n#.#.##.#.', '#...##..#\n#....#..#\n..##..###\n#####.##.\n#####.##.\n..##..###\n#....#..#']
test_input_2 = ['#.##..##.\n..#.##.#.\n##......#\n##......#\n..#.##.#.\n..##..##.\n#.#.##.#.', '#...##..#\n#....#..#\n..##..###\n#####.##.\n#####.##.\n..##..###\n#....#..#', '.#.##.#.#\n.##..##..\n.#.##.#..\n#......##\n#......##\n.#.##.#..\n.##..##.#', '#..#....#\n###..##..\n.##.#####\n.##.#####\n###..##..\n#..#....#\n#..##...#', '#.##..##.\n..#.##.#.\n##..#...#\n##...#..#\n..#.##.#.\n..##..##.\n#.#.##.#.']

row_reflections, col_reflections = 0, 0
for grid in input_data[:]:
    grid_array = np.array([list(row) for row in grid.split('\n')])

    # Check Vertical Reflection
    reflection_point = check_reflection(grid_array)
    col_reflections += reflection_point
    if reflection_point == 0: # No Vertical Reflection
        transposed_grid = np.transpose(grid_array)
        # Check Horizontal Reflection
        row_reflections += (100 * check_reflection(transposed_grid))

print("Part 1:", (col_reflections + row_reflections))
