# Advent of Code - Day 1, Year 2020
# Solution Started: Nov 19, 2024
# Puzzle Link: https://adventofcode.com/2020/day/1
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D01_file = "Day01_input.txt"
D01_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D01_file)

# Read and sort input data into a grid
with open(D01_file_path) as file:
    input_data = file.read().strip().split('\n')
    num_list = [int(num) for num in input_data]

for n1 in num_list:
    for n2 in num_list:
        sum_check = n1 + n2
        if sum_check == 2020:
            ans_p1 = n1 * n2

print(f"Part 1: {ans_p1}")

for n1 in num_list:
    for n2 in num_list:
        for n3 in num_list:
            sum_check = n1 + n2 + n3
            if sum_check == 2020:
                ans_p2 = n1 * n2 * n3

print(f"Part 2: {ans_p2}")

# Increase speed using sets