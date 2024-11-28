# Advent of Code - Day 3, Year 2022
# Solution Started: Nov 28, 2024
# Puzzle Link: https://adventofcode.com/2022/day/3
# Solution by: [abbasmoosajee07]
# Brief: [Rucksacks and Unique Letters]

#!/usr/bin/env python3

import os, re, copy, string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the input data from the specified file path
D03_file = "Day03_input.txt"
D03_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D03_file)

# Read and sort input data into a grid
with open(D03_file_path) as file:
    input_data = file.read().strip().split('\n')

def split_str_in_middle(str):
    # Convert str to list
    lst = list(str)
    # Calculate the middle index
    mid = len(lst) // 2
    # Split the list into two halves
    first_half = lst[:mid]
    second_half = lst[mid:]
    return first_half, second_half

def calc_total_priority(rucksack_list):
    lowercase_priority = {letter: index
                    for index, letter in enumerate(string.ascii_lowercase, start=1)}
    uppercase_priority = {letter: index
                        for index, letter in enumerate(string.ascii_uppercase, start=27)}
    # Merging dictionaries using update()
    letter_priority = lowercase_priority.copy()  # Create a copy of the first dictionary
    letter_priority.update(uppercase_priority)
    total_priorities = 0
    for rucksack in rucksack_list:
        joined_rucksack = rucksack
        compartment_1, compartment_2 = split_str_in_middle(rucksack)
        count_1 = Counter(compartment_1)
        count_2 = Counter(compartment_2)
        for key in count_1:
            if key in count_2:
                total_priorities += letter_priority[key]
    return total_priorities

ans_p1 = calc_total_priority(input_data)
print("Part 1:", ans_p1)


def calc_priority_grouped_elves(rucksack_list, group_by = 1):
    lowercase_priority = {letter: index
                    for index, letter in enumerate(string.ascii_lowercase, start=1)}
    uppercase_priority = {letter: index
                        for index, letter in enumerate(string.ascii_uppercase, start=27)}
    # Merging dictionaries using update()
    letter_priority = lowercase_priority.copy()  # Create a copy of the first dictionary
    letter_priority.update(uppercase_priority)
    total_priorities = 0
    for pos in range(0, len(rucksack_list), group_by):
        grouped_rucksacks = rucksack_list[pos:pos + group_by]
        count_list = []
        for rucksack_n in grouped_rucksacks:
            count_list.append(Counter(list(rucksack_n)))
        # Find the intersection of all dictionaries (keys that are present in all)
        common_keys = set(count_list[0].keys())  # Start with the keys from the first dictionary
        
        # Find common keys across all dictionaries
        for count in count_list[1:]:
            common_keys &= set(count.keys())  # Keep only keys that are in all dictionaries
        
        # Add the priorities for the common keys
        for key in common_keys:
            total_priorities += letter_priority.get(key, 0)  # Add the priority from letter_priority
        
    return total_priorities
ans_p2 = calc_priority_grouped_elves(input_data, group_by = 3)
print("Part 2:", ans_p2)