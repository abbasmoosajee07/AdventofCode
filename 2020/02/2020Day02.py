# Advent of Code - Day 2, Year 2020
# Solution Started: Nov 19, 2024
# Puzzle Link: https://adventofcode.com/2020/day/2
# Solution by: [abbasmoosajee07]
# Brief: [Valid Passwords]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
# Load the input data from the specified file path
D02_file = "Day02_input.txt"
D02_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D02_file)

# Read and sort input data into a grid
with open(D02_file_path) as file:
    input_data = file.read().strip().split('\n')

def password_criteria(input_list):
    criteria_list = []
    # Process each password condition entry in the list
    for criteria in input_list:
        condition, password = criteria.split(': ')
        range, letter = condition.split(' ')
        n1, n2 = range.split('-')
        criteria_n = [int(n1), int(n2), letter, list(password)]
        criteria_list.append(criteria_n)
    return criteria_list

def count_valid_passwords(criteria_list):
    count = 0
    for possible_password in criteria_list:
        min, max = possible_password[0], possible_password[1]
        key_letter = possible_password[2]
        password = possible_password[3]

        str_count = dict(Counter(password))
        if key_letter in str_count:
            key_count = str_count[key_letter]
            if min <= key_count <= max:
                count += 1
    return count

input_criteria = password_criteria(input_data)
ans_p1 = count_valid_passwords(input_criteria)
print(f"Part 1: {ans_p1}")

def count_tca_passwords(criteria_list):
    count = 0
    for possible_password in criteria_list:
        pos_1, pos_2 = possible_password[0], possible_password[1]
        key_letter = possible_password[2]
        password = possible_password[3]
        
        if key_letter in password:
            # pos - 1 to correct for zero index
            if password[pos_1 - 1] == key_letter:
                if password[pos_2 - 1] != key_letter: # make sure not present in both
                    count += 1
            # pos - 1 to correct for zero index
            elif password[pos_2 - 1] == key_letter:
                count += 1

    return count

ans_p2 = count_tca_passwords(input_criteria)
print(f"Part 2: {ans_p2}")