"""Advent of Code - Day 25, Year 2022
Solution Started: Dec 15, 2024
Puzzle Link: https://adventofcode.com/2022/day/25
Solution by: abbasmoosajee07
Brief: [SNAFU Numbers]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D25_file = "Day25_input.txt"
D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

# Read and sort input data into a grid
with open(D25_file_path) as file:
    input_data = file.read().strip().split('\n')

def SNAFU_to_decimal(snafu_num):
    snafu_list = list(snafu_num)[::-1]
    decimal_num = 0
    for pos, char in enumerate(snafu_list):
        pos_power = 5 ** pos
        if char.isdigit():
            decimal_num += (pos_power * int(char))
        elif char == '-':
            decimal_num += (pos_power * -1)
        elif char == '=':
            decimal_num += (pos_power * -2)
    return decimal_num

def decimal_to_SNAFU(decimal_num):
    snafu_digits = []  # Stores the resulting SNAFU digits

    while decimal_num != 0:
        remainder = decimal_num % 5  # Find remainder when dividing by 5

        if remainder == 0:
            snafu_digits.append('0')
            carry = 0
        elif remainder == 1:
            snafu_digits.append('1')
            carry = 0
        elif remainder == 2:
            snafu_digits.append('2')
            carry = 0
        elif remainder == 3:  # Convert 3 into '-2' with a carry of +1
            snafu_digits.append('=')
            carry = 2
        elif remainder == 4:  # Convert 4 into '-1' with a carry of +1
            snafu_digits.append('-')
            carry = 1
        
        # Adjust the number for the next iteration
        decimal_num = (decimal_num + carry) // 5

    # Join the digits and reverse to form the final SNAFU number
    return ''.join(snafu_digits[::-1])



total_sum = 0
for num_str in input_data:
    total_sum += SNAFU_to_decimal(num_str)
snafu_sum = decimal_to_SNAFU(total_sum)
print("Final Problem:", snafu_sum) # 2=-1=0