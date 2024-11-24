# Advent of Code - Day 14, Year 2021
# Solution Started: Nov 24, 2024
# Puzzle Link: https://adventofcode.com/2021/day/14
# Solution by: [abbasmoosajee07]
# Brief: [Polymerization]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# Load the input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

# Read and sort input data into a grid
with open(D14_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    initial_polymer = input_data[0].strip()
    insertion_rules = input_data[1].split('\n')

def parse_to_dict(strings):
    result = {}
    for string in strings:
        key, values = string.split(" -> ", 1)
        result[key] = values
    return result

def polymerization(initial_polymer, insertion_rules, steps):
    """
    Perform polymerization using the pair frequency approach.
    - initial_polymer: The initial polymer string.
    - insertion_rules: A dictionary of pair -> element mappings.
    - steps: Number of polymerization steps to perform.
    """
    # Count initial pairs
    pair_counts = Counter(
        initial_polymer[i:i+2] for i in range(len(initial_polymer) - 1)
    )
    # Count initial elements
    element_counts = Counter(initial_polymer)

    # Perform polymerization steps
    for _ in range(steps):
        new_pair_counts = defaultdict(int)
        for pair, count in pair_counts.items():
            if pair in insertion_rules:
                # Get the element to insert
                insert_element = insertion_rules[pair]
                # Update element counts
                element_counts[insert_element] += count
                # Update pair counts for the new pairs
                new_pair_counts[pair[0] + insert_element] += count
                new_pair_counts[insert_element + pair[1]] += count
            else:
                # No rule for this pair, keep the original
                new_pair_counts[pair] += count
        pair_counts = new_pair_counts

    return element_counts

def calculate_difference(element_counts):
    """Calculate the difference between the most and least common elements."""
    most_common = max(element_counts.values())
    least_common = min(element_counts.values())
    return most_common - least_common

insertion_dict = parse_to_dict(insertion_rules)

# Part 1: Perform 10 steps
element_counts_part1 = polymerization(initial_polymer, insertion_dict, 10)
result_part1 = calculate_difference(element_counts_part1)
print(f"Part 1: {result_part1}")

# Part 2: Perform 40 steps
element_counts_part2 = polymerization(initial_polymer, insertion_dict, 40)
result_part2 = calculate_difference(element_counts_part2)
print(f"Part 2: {result_part2}")
