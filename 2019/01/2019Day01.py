# Advent of Code - Day 1, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/1
# Solution by: [abbasmoosajee07]
# Brief: [Fuel Calculator]

#!/usr/bin/env python3

import os, re, copy, math
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

def fuel_calc(mass):
    return  math.floor(mass / 3) - 2

def calc_fuel_required(input, negative=False):

    total_fuel = 0
    for num in input:
        fuel = fuel_calc(num)
        if not negative:
            # Add only the initial fuel
            total_fuel += max(fuel, 0)  # Ignore negative fuel
        else:
            # Add fuel recursively until it becomes zero or negative
            while fuel > 0:
                total_fuel += fuel
                fuel = fuel_calc(fuel)  # Calculate fuel for the new fuel
    return total_fuel


ans_p1 = calc_fuel_required(input_list)

print(f"Part 1: {ans_p1}")


ans_p2 = calc_fuel_required(input_list, negative=True)

print(f"Part 1: {ans_p2}")