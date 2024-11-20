# Advent of Code - Day 4, Year 2020
# Solution Started: Nov 20, 2024
# Puzzle Link: https://adventofcode.com/2020/day/4
# Solution by: [abbasmoosajee07]
# Brief: [Valid Passports]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the input data from the specified file path
D04_file = "Day04_input.txt"
D04_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D04_file)

# Read and sort input data into a grid
with open(D04_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_to_dict(input_list):
    passport_list = []
    for entry in input_list:
        dict = {}
        for line in entry.split('\n'):
            for string in line.split(' '):
                key, values = string.split(":", 1)
                dict[key] = values.split(",")
        passport_list.append(dict)
    return passport_list

def passport_condition_p1(passport):
    len_dict = len(passport)
    if len_dict == 8:
        return 1
    elif len_dict == 7:
        if 'cid' not in passport.keys():
            return 1
        else:
            return 0
    else:
        return 0

def count_valid_passports(passport_dict, passport_func):
    valid_count = 0
    for passport in passport_dict:
        validity = passport_func(passport)
        if validity is not None:
            valid_count += validity
    return valid_count

passport_dict = parse_to_dict(input_data)
ans_p1 = count_valid_passports(passport_dict, passport_condition_p1)
print(f"Part 1: {ans_p1}")

def passport_condition_p2(passport):
    # Check for required fields
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    if not all(field in passport for field in required_fields):
        return 0

    try:
        # Validate each field
        byr = int(passport['byr'][0])
        if not (1920 <= byr <= 2002):
            return 0

        iyr = int(passport['iyr'][0])
        if not (2010 <= iyr <= 2020):
            return 0

        eyr = int(passport['eyr'][0])
        if not (2020 <= eyr <= 2030):
            return 0

        hgt = passport['hgt'][0]
        if hgt.endswith('cm'):
            height = int(hgt[:-2])
            if not (150 <= height <= 193):
                return 0
        elif hgt.endswith('in'):
            height = int(hgt[:-2])
            if not (59 <= height <= 76):
                return 0
        else:
            return 0

        hcl = passport['hcl'][0]
        if not re.fullmatch(r'#[0-9a-f]{6}', hcl):
            return 0

        ecl = passport['ecl'][0]
        if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return 0

        pid = passport['pid'][0]
        if not re.fullmatch(r'\d{9}', pid):
            return 0

        return 1  # All validations passed
    except (ValueError, KeyError):
        return 0

ans_p2 = count_valid_passports(passport_dict, passport_condition_p2)
print(f"Part 2: {ans_p2}")