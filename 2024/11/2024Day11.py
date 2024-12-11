"""Advent of Code - Day 11, Year 2024
Solution Started: Dec 11, 2024
Puzzle Link: https://adventofcode.com/2024/day/11
Solution by: abbasmoosajee07
Brief: [Exponentially Increasing lists]
"""

#!/usr/bin/env python3

import os, re, copy
from itertools import chain
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path) as file:
    input_data = file.read().strip().split(' ')

def split_by_digits(num):
    num_str = str(num)
    mid = len(num_str) // 2
    part1 = num_str[:mid] if mid > 0 else '0'
    part2 = num_str[mid:] if mid < len(num_str) else '0'
    return str(int(part1)), str(int(part2))

def stone_rules(stone_counts):
    """
    Apply stone transformation rules and return the updated stone counts.
    """
    next_stone_counts = Counter()

    # For each type of stone, process the transformation
    for stone, count in stone_counts.items():
        if int(stone) == 0:
            # Replace 0 with 1
            next_stone_counts['1'] += count
        elif len(stone) % 2 == 0:
            # Split the stone with an even number of digits
            num_1, num_2 = split_by_digits(stone)
            next_stone_counts[num_1] += count
            next_stone_counts[num_2] += count
        else:
            # Multiply the stone by 2024
            new_stone = str(int(stone) * 2024)
            next_stone_counts[new_stone] += count

    return next_stone_counts

def simulate_blinking(init_list, total_blinks=25):
    # Initialize the stone counts using a Counter
    stone_counts = Counter(init_list)
    
    # Simulate the blinking process for the specified number of days (blinks)
    for blink in range(total_blinks):
        # Apply the stone rules to update the stone counts
        stone_counts = stone_rules(stone_counts)
        # print(f"{blink=} {stone_counts}")
    # Return the total number of stones after the simulation
    return sum(stone_counts.values())

# Part 1 (simulate for 25 blinks)
part1 = simulate_blinking(input_data, total_blinks=25)
print("Part 1:", part1)

# Part 2 (simulate for 75 blinks)
part2 = simulate_blinking(input_data, total_blinks=75)
print("Part 2:", part2)
