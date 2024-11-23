# Advent of Code - Day 6, Year 2021
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2021/day/6
# Solution by: [abbasmoosajee07]
# Brief: [Simulate Fish Growth]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
# Load the input data from the specified file path
D06_file = "Day06_input.txt"
D06_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D06_file)

# Read and sort input data into a grid
with open(D06_file_path) as file:
    input_data = file.read().strip().split(',')
    num_list = [int(num) for num in input_data]

def  daily_fish_growth(fish_list):
    next_day = fish_list[:]
    for idx, fish in enumerate(fish_list):
        if fish == 0:
            next_day[idx] = 6
            next_day.append(8)
        else:
            next_day[idx] = fish - 1
    return next_day

initial_state = num_list
new_day = initial_state
total_days = 80

for day in range(1, total_days + 1, 1):
    new_day = daily_fish_growth(new_day)
    # print(f"Day {day}: {new_day}")

print("Part 1:", len(new_day))

# Count initial numbers of lanternfish at each age
lanternfish = num_list
lf_counts = Counter(lanternfish)
lf_counts = {age: lf_counts.get(age, 0) for age in range(9)}  # Ensure keys for ages 0-8

nDays = 256  # A: 80 / B: 256

for _ in range(nDays):
    # Number of fish producing new ones
    new_fish = lf_counts[0]

    # Shift all ages down by 1 day
    lf_counts = {age: lf_counts[age + 1] if age < 8 else 0 for age in range(9)}

    # Add new fish to age 8 and reset producers to age 6
    lf_counts[6] += new_fish
    lf_counts[8] += new_fish

# Total number of lanternfish
print("Part 2:", sum(lf_counts.values()))