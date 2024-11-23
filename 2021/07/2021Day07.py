# Advent of Code - Day 7, Year 2021
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2021/day/7
# Solution by: [abbasmoosajee07]
# Brief: [Fuel Requirements]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and sort input data into a grid
with open(D07_file_path) as file:
    input_data = file.read().strip().split(',')
    num_list = [int(num) for num in input_data]
    
def sum_all_differences(a, b):
    # Find the absolute difference
    diff = abs(a - b)
    
    # Calculate the sum of all differences
    # Using the formula for sum of first n numbers
    return diff * (diff + 1) // 2

def fuel_required(position_list):
    fuel_p1 = set()
    fuel_p2 = set()

    for pos_x in position_list:
        fuel_n1 = 0
        fuel_n2 = 0
        for pos_n in position_list:
            fuel_n1 += abs(pos_n - pos_x)
            fuel_n2 += sum_all_differences(pos_n, pos_x)
        fuel_p1.add(fuel_n1)
        fuel_p2.add(fuel_n2)
    return fuel_p1, fuel_p2

fuel_p1, fuel_p2 = fuel_required(num_list)
print("Part 1:", min(fuel_p1))
print("Part 2:", min(fuel_p2))

