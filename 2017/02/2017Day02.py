# Advent of Code - Day 2, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/2
# Solution by: [abbasmoosajee07]
# Brief: [Handling number tables]

import os
import re
import pandas as pd
import numpy as np

D2_file = 'Day02_input.txt'
D2_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D2_file)

with open(D2_file_path) as file:
    input = file.read().splitlines()
    input_grid = np.zeros((len(input), len(input[0])))

    for row in range(len(input)):
        row_list = input[row].split()
        for col in range(len(row_list)):
            num = int(row_list[col])
            input_grid[row][col] = num

def maxmin_checksum(num_grid):
    checksum = 0
    
    for row in num_grid:
        row_max = np.max(row[np.nonzero(row)])
        row_min = np.min(row[np.nonzero(row)])
        row_diff = row_max - row_min
        checksum += row_diff
    return checksum

P1_checksum = maxmin_checksum(input_grid)
print(f"Part 1: The checksum of input grid is: {P1_checksum}")

# First Guess: 33696, too high
# Correct: 32121 had to ignore zero

def divisible_checksum(num_grid):
    checksum = 0

    # Iterate over each row in num_grid
    for row in num_grid:
        # Loop through all pairs of numbers (num, value) in the row
        for i in range(len(row)):
            num = row[i]
            if not np.isfinite(num) or num == 0:  # Skip NaN, inf, and zero
                continue
            
            for j in range(len(row)):
                value = row[j]
                if i != j and np.isfinite(value) and value != 0:  # Check for valid value and avoid division by zero
                    if num % value == 0:  # Check if num is divisible by value
                        checksum += num // value  # Add the result of division to the checksum
                        break  # No need to check further once a divisible pair is found

    return checksum

P2_checksum = divisible_checksum(input_grid)
print(f"Part 2: The checksum of input grid is: {P2_checksum}")

# First Guess: 141444, too high
# Second Guess: 300058 too high
# Third Guess: 453 too high
# Correct: 197 had to ignore itself 