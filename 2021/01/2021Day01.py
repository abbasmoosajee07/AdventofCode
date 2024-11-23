# Advent of Code - Day 1, Year 2021
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2021/day/1
# Solution by: [abbasmoosajee07]
# Brief: [Measurements Relative to the past]

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
    input_list = [int(num) for num in input_data]

increased = 0

for idx in range(1 ,len(input_list), 1):
    prev_no = input_list[idx - 1]
    curr_no = input_list[idx]
    if curr_no > prev_no:
        increased += 1

print("Part 1:", increased)

increased_sum = 0
for idx in range(1 ,len(input_list), 1):
    if idx + 3 > len(input_list):
        break
    else:
        prev_sum = sum(input_list[idx - 1:idx+2])
        curr_sum = sum(input_list[idx:idx+3])

        if curr_sum > prev_sum:
            increased_sum += 1

print("Part 2:", increased_sum)
