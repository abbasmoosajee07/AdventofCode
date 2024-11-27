# Advent of Code - Day 25, Year 2021
# Solution Started: Nov 27, 2024
# Puzzle Link: https://adventofcode.com/2021/day/25
# Solution by: [abbasmoosajee07]
# Brief: [Modelling Fish to a Constant State]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D25_file = "Day25_input.txt"
D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

# Read and sort input data into a grid
with open(D25_file_path) as file:
    input_data = file.read().strip().split('\n')

def model_fish(initial_grid):
    """
    Simulates the movement of fish in a grid, where '>' represents eastward swimming fish,
    and 'v' represents southward swimming fish. The function runs the simulation until no fish
    move and returns the number of steps it took for this to happen.

    :param initial_grid: A list of strings representing the initial grid of fish.
    :return: The number of steps until no fish move.
    """
    
    width, height = len(initial_grid[0]), len(initial_grid)  # grid dimensions (width x height)

    steps = 0  # Initialize the step counter
    finished = False  # Flag to track if no fish moved during the step

    # Continue running until no fish move
    while not finished:
        finished = True  # Assume all fish are finished, we will check if any moved

        # Step 1: Process Eastward swimming fish ('>')
        new_grid = []
        for row in initial_grid:
            # Look for '>.', meaning an eastward fish that can move
            if row[width - 1] + row[0] == '>.':
                # Move fish, filling with 'p' temporarily to manage swaps
                row = 'p' + row[1:width - 1] + ':'  # temporarily modify the row
            # Replace '>.', ':', and 'p' to get the new row after the move
            new_row = row.replace('>.', '.>') \
                            .replace(':', '.') \
                            .replace('p', '>')
            new_grid.append(new_row)
            # Check if the row was modified; if so, fish moved
            if new_row != row:
                finished = False  # Fish moved, not finished yet

        # Step 2: Process Southward swimming fish ('v')
        # Transpose the grid to handle vertical movement
        transposed_grid = [''.join(row) for row in zip(*new_grid)]  # Transpose grid

        new_grid = []
        for row in transposed_grid:
            # Look for 'v.', meaning a southward fish that can move
            if row[height - 1] + row[0] == 'v.':
                # Move fish, filling with 'p' temporarily to manage swaps
                row = 'p' + row[1:height - 1] + ':'  # temporarily modify the row
            # Replace 'v.', ':', and 'p' to get the new row after the move
            new_row = row.replace('v.', '.v') \
                            .replace(':', '.') \
                            .replace('p', 'v')
            new_grid.append(new_row)
            # Check if the row was modified; if so, fish moved
            if new_row != row:
                finished = False  # Fish moved, not finished yet

        # Transpose back to restore original grid orientation
        initial_grid = [''.join(row) for row in zip(*new_grid)]

        # Increment the step counter
        steps += 1

    return steps  # Return the number of steps it took until no fish moved


ans = model_fish(input_data)
print("Part 1:", ans)