"""Advent of Code - Day 13, Year 2023
Solution Started: Jan 1, 2025
Puzzle Link: https://adventofcode.com/2023/day/13
Solution by: abbasmoosajee07
Brief: [Checking Reflections]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

# Read and sort input data into a grid
with open(D13_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def identify_reflection(init_grid: list, reflection_func: str) -> int:
    pattern_len = len(init_grid)
    for pos in range(1, pattern_len):
        reflection_span = min(pos, pattern_len-pos)
        # Define the base and reflected patterns
        base_pattern = init_grid[pos-reflection_span:pos]
        reflected_pattern = init_grid[pos:pos+reflection_span][::-1]
        if reflection_func == 'find':
            # Check if patterns are equal
            if np.array_equal(base_pattern, reflected_pattern):
                return pos
        elif reflection_func == 'fix':
            # Identify the new reflection point
            if (base_pattern != reflected_pattern).sum() == 1:
                return pos
    return None

def check_reflections(grid: list, reflection_function:str = 'find') -> int:
    """ Check for horizontal and vertical reflections in the grid. """

    # Check horizontal reflection
    horizontal_reflection = identify_reflection(grid, reflection_function)
    if horizontal_reflection:
        return horizontal_reflection * 100

    # Check vertical reflection (transpose for column comparison)
    vertical_reflection = identify_reflection(grid.T, reflection_function)
    if vertical_reflection:
        return vertical_reflection
    return 0

reflections_p1, reflections_p2 = 0, 0

for grid in input_data[:]:
    grid_array = np.array([list(row) for row in grid.split('\n')])
    reflections_p1 += check_reflections(grid_array, 'find')
    reflections_p2 += check_reflections(grid_array, 'fix')

print("Part 1:", reflections_p1)
print("Part 2:", reflections_p2)

# print(f"Execution Time = {time.time() - start_time:.5f}s")

