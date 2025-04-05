"""Advent of Code - Day 24, Year 2015
Solution Started: Apr 5, 2025
Puzzle Link: https://adventofcode.com/2015/day/24
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os
from itertools import combinations
from math import prod

# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read and sort input data into a grid
with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n')
    package_list = [int(num) for num in input_data]

def create_package_combo(packages: list, group_no):
    packages = [int(x) for x in packages]
    target_sum = sum(packages) // group_no

    # Find all combinations that sum to the target
    package_combinations = []
    for r in range(1, len(packages) + 1):
        valid_combos = [list(combo) for combo in combinations(packages, r) if sum(combo) == target_sum]
        if valid_combos:
            package_combinations.extend(valid_combos)
            break  # only smallest group size combinations needed first

    # Find minimal length group(s)
    min_length = min(len(combo) for combo in package_combinations)
    group_contenders = [combo for combo in package_combinations if len(combo) == min_length]

    quantum_entanglement = min(prod(contender) for contender in group_contenders)
    return quantum_entanglement

group_3 = create_package_combo(package_list, 3)
print("Part 1:", group_3)

group_4 = create_package_combo(package_list, 4)
print("Part 2:", group_4)