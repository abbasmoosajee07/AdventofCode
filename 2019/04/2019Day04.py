# Advent of Code - Day 4, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/4
# Solution by: [abbasmoosajee07]
# Brief: [Counting Valid Passwords]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
from collections import Counter

# Load the input data from the specified file path
D04_file = "Day04_input.txt"
D04_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D04_file)

# Read and sort input data into a grid
with open(D04_file_path) as file:
    input_data = file.read().strip().split('\n')

def check_valid_password(number):
    # Convert the number to a string for digit manipulation
    num_str = str(number)
    
    # Check if the number has exactly 6 digits
    if len(num_str) != 6:
        return [0, 0]
    
    has_adjacent = False  # To check for at least one pair of identical consecutive digits
    
    # Iterate through the digits to check conditions
    for i in range(1, len(num_str)):
        # Check if digits decrease (non-increasing order invalidates the password)
        if num_str[i] < num_str[i - 1]:
            return [0, 0]
        # Check for adjacent digits
        if num_str[i] == num_str[i - 1]:
            has_adjacent = True

    # The password is valid if there's at least one pair of identical digits
    if has_adjacent:
        num_count = Counter(num_str)
        if 2 in num_count.values():
            return [1, 1]
        else:
            return [1, 0]
    else:
        return [0, 0]

def count_valid_password(min_num, max_num):
    count_p1 = 0
    count_p2 = 0

    for num in range(min_num, max_num, 1):
        valid_password = check_valid_password(num)
        count_p1 += valid_password[0]
        count_p2 += valid_password[1]

    return count_p1, count_p2

num_range = input_data[0].split('-')
min_num = int(num_range[0])
max_num = int(num_range[1])

ans_p1, ans_p2 = count_valid_password(min_num, max_num)
print(f"Part 1: {ans_p1}")
print(f"Part 2: {ans_p2}")
