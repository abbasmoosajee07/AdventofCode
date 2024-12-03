"""Advent of Code - Day 3, Year 2024
Solution Started: Dec 3, 2024
Puzzle Link: https://adventofcode.com/2024/day/3
Solution by: abbasmoosajee07
Brief: [Regex and activating multiplication]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D03_file = "Day03_input.txt"
D03_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D03_file)

# Read and sort input data into a grid
with open(D03_file_path) as file:
    input_data = file.read().strip().split('\n')
# print(input_data)

def find_muls(input_list):
    """
    Finds all 'mul(a,b)' patterns in the input strings, computes their products, 
    and returns the sum of these products.

    Args:
    - input_data: list of strings, each containing potential 'mul(a,b)' patterns.

    Returns:
    - int, sum of all products from the 'mul(a,b)' patterns.
    """
    pattern = r"mul\((-?\d+),(-?\d+)\)"
    total_sum = 0

    for line in input_list:
        matches = re.findall(pattern, line)
        for n1, n2 in matches:
            total_sum += int(n1) * int(n2)

    return total_sum

ans_p1 = find_muls(input_data)
print("Part 1:", ans_p1)


def find_muls_with_activation(input_list):
    """
    Extracts all occurrences of 'mul(a,b)', 'do()', and 'don't()' in the order they appear,
    processes them to calculate the total sum of valid multiplications based on activation states.

    Args:
    - input_list: list of str, the input strings to search.

    Returns:
    - int: The total sum of valid multiplications.
    """
    total_sum = 0
    activation = 1  # Start with activation enabled
    patterns = [
        r"mul\((-?\d+),(-?\d+)\)",  # Matches 'mul(a,b)'
        r"do\(\)",                 # Matches 'do()'
        r"don't\(\)"               # Matches "don't()"
    ]

    # Process each line in order
    for line in input_list:
        # Find all matches for the patterns, keeping order
        matches = []
        for pattern in patterns:
            for match in re.finditer(pattern, line):
                matches.append((match.group(), match.start()))

        # Sort matches by their position in the string
        matches.sort(key=lambda x: x[1])

        # Process matches in order
        for match, _ in matches:
            if match.startswith("do()"):
                activation = 1  # Enable activation
            elif match.startswith("don't()"):
                activation = 0  # Disable activation
            elif match.startswith("mul"):
                n1, n2 = map(int, re.findall(r"-?\d+", match))
                if activation == 1:  # Only add to sum if activated
                    total_sum += (n1 * n2)
    
    return total_sum

ans_p2 = find_muls_with_activation(input_data)
print("Part 2:", ans_p2)