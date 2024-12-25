"""Advent of Code - Day 25, Year 2024
Solution Started: Dec 25, 2024
Puzzle Link: https://adventofcode.com/2024/day/25
Solution by: abbasmoosajee07
Brief: [Match Lock and key]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the input data from the specified file path
D25_file = "Day25_input.txt"
D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

# Read and sort input data into a grid
with open(D25_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def find_heights(lock_grid: str):

    # Convert the lock grid string into a 2D NumPy array
    schematic_array = np.array([list(row) for row in lock_grid.strip().split('\n')], dtype=object)

    # Determine schematic type based on first and last row
    schematic_type = None
    if ''.join(schematic_array[0]) == '#####':  # Example condition for "lock"
        schematic_type = 'lock'
    elif ''.join(schematic_array[-1]) == '#####':  # Example condition for "key"
        schematic_type = 'key'
    else:
        raise ValueError("Unable to determine schematic type. Check the input grid format.")

    # Transpose the grid to analyze columns
    transposed_schematic = np.transpose(schematic_array)
    all_heights = []

    # Calculate the height for each column
    for row in transposed_schematic:
        row_count = dict(Counter(row))
        height = row_count.get('#', 0) - 1  # Ensure height defaults to 0 if `count` is not in the row
        all_heights.append(height)

    return schematic_type, all_heights

def classify_schematics(schematics: list[str]):

    lock_dict, lock_no, key_dict, key_no = {}, 0, {}, 0

    for schematic in schematics:
        schematic_type, heights = find_heights(schematic)
        if schematic_type == 'lock':
            lock_no += 1
            lock_dict[lock_no] = heights
        elif schematic_type == 'key':
            key_no += 1
            key_dict[key_no] = heights

    return lock_dict, key_dict

def match_lock_key(lock_dict: dict, key_dict: dict) -> int:
    total_matches = 0
    for lock_no, lock_heights in lock_dict.items():
        for key_no, key_heights in key_dict.items():
            valid_match = True
            for pos, height in enumerate(lock_heights):
                total_height = height + key_heights[pos]
                if total_height > 5:
                    valid_match = False
                    break
            if valid_match is True:
                total_matches += 1
    return total_matches


lock_dict, key_dict = classify_schematics(input_data)
all_matches = match_lock_key(lock_dict, key_dict)
print("Part 1:", all_matches)

