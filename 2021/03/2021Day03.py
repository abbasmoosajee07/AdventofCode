# Advent of Code - Day 3, Year 2021
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2021/day/3
# Solution by: [abbasmoosajee07]
# Brief: [Binary and Decimal Numbers]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D03_file = "Day03_input.txt"
D03_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D03_file)

# Read and sort input data into a grid
with open(D03_file_path) as file:
    input_data = file.read().strip().split('\n')
    num_array = np.array([
                    [int(num) for num in list(row)]
                        for row in input_data])

def find_gamma_epsilon(binary_array):
    rows, cols = np.shape(binary_array)
    gamma = []
    epsilon = []
    for col_no in range(cols):
        column = binary_array[:,col_no]
        zero_count = sum(1 for x in column if x == 0)
        one_count  = sum(1 for x in column if x == 1)
        count_dict = {'0':zero_count, '1': one_count}

        # Find the key with the maximum count and append
        gamma_val = max(count_dict, key=count_dict.get)
        gamma.append(gamma_val)

        # Find the key with the minimum count and append
        epsilon_val = min(count_dict, key=count_dict.get)
        epsilon.append(epsilon_val)

        gamma_dec = int(''.join(gamma),2)
        epsilon_dec = int(''.join(epsilon),2)

    return gamma_dec * epsilon_dec

ans_p1 = find_gamma_epsilon(num_array)
print("Part 1:", ans_p1)

def find_life_support_rating(binary_array_init, function):
    rows, cols = np.shape(binary_array_init)
    binary_array = np.copy(binary_array_init)  # Use np.copy for safety
    support_system = []

    for col_no in range(cols):
        column = binary_array[:, col_no]
        zero_count = sum(1 for x in column if x == 0)
        one_count  = sum(1 for x in column if x == 1)
        count_dict = {'0': zero_count, '1': one_count}

        # Determine the value to keep with the tiebreaker rule
        if zero_count == one_count:
            # Tiebreaker: prefer 1 for max, 0 for min
            element_val = '1' if function == max else '0'
        else:
            element_val = function(count_dict, key=count_dict.get)
        
        support_system.append(str(element_val))

        # Filter rows based on the column value
        binary_array = binary_array[binary_array[:, col_no] == int(element_val)]

        # Stop if only one row is left
        if len(binary_array) == 1:
            break

    # Use the remaining row for the rating if available
    if len(binary_array) == 1:
        rating = int(''.join(map(str, binary_array[0])), 2)
    else:
        rating = int(''.join(support_system), 2)

    return rating


o2_gen = find_life_support_rating(num_array, max)
co2_scrub = find_life_support_rating(num_array, min)
ans_p2 = o2_gen * co2_scrub
print("Part 2:", ans_p2)
