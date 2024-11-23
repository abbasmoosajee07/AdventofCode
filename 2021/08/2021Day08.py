# Advent of Code - Day 8, Year 2021
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2021/day/8
# Solution by: [abbasmoosajee07]
# Brief: [Decoding Strings to Numbers]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the input data from the specified file path
D08_file = "Day08_input.txt"
D08_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D08_file)

# Read and sort input data into a grid
with open(D08_file_path) as file:
    input_data = file.read().strip().split('\n')

def count_digits_1478(input):
    valid_digits = 0
    for line in input:
        easy_digits = line.split(' | ')[1]
        for digit in easy_digits.split(' '):
            str_len = len(list(digit))
            if str_len in [2, 3, 4, 7]:
                valid_digits += 1
    return valid_digits

ans_p1 = count_digits_1478(input_data)
print("Part 1:", ans_p1)

def decode_signal(signal_patterns, output_values):
    # Step 1: Sort and group the patterns by length
    signal_patterns = [''.join(sorted(p)) for p in signal_patterns]
    output_values = [''.join(sorted(o)) for o in output_values]

    # Map to find the unique numbers
    patterns_by_length = {len(p): [] for p in signal_patterns}
    for pattern in signal_patterns:
        patterns_by_length[len(pattern)].append(pattern)

    # Deduce the unique digits
    number_map = {}
    number_map[1] = patterns_by_length[2][0]  # Unique length 2
    number_map[4] = patterns_by_length[4][0]  # Unique length 4
    number_map[7] = patterns_by_length[3][0]  # Unique length 3
    number_map[8] = patterns_by_length[7][0]  # Unique length 7

    # Step 2: Identify other digits by overlap
    for pattern in patterns_by_length[5]:  # Digits 2, 3, 5 have length 5
        if all(c in pattern for c in number_map[1]):
            number_map[3] = pattern
        elif len(set(pattern) & set(number_map[4])) == 3:
            number_map[5] = pattern
        else:
            number_map[2] = pattern

    for pattern in patterns_by_length[6]:  # Digits 0, 6, 9 have length 6
        if all(c in pattern for c in number_map[4]):
            number_map[9] = pattern
        elif all(c in pattern for c in number_map[1]):
            number_map[0] = pattern
        else:
            number_map[6] = pattern

    # Step 3: Invert the map to decode output values
    reverse_map = {v: k for k, v in number_map.items()}
    decoded_output = [reverse_map[o] for o in output_values]
    return int(''.join(map(str, decoded_output)))

def decode_letters_to_num(input):
    total_sum = 0
    for line in input:
        decoder, digits = line.split(' | ')
        decoder_list = decoder.split(' ')
        digits_list = digits.split(' ')
        decoded_number = decode_signal(decoder_list, digits_list)
        total_sum += decoded_number
    return total_sum

ans_p2 = decode_letters_to_num(input_data)
print("Part 2:", ans_p2)