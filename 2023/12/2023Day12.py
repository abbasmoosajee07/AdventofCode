"""Advent of Code - Day 12, Year 2023
Solution Started: Dec 28, 2024
Puzzle Link: https://adventofcode.com/2023/day/12
Solution by: abbasmoosajee07
Brief: [Filling the blanks]
"""

#!/usr/bin/env python3

import os, re, copy, sys, functools, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()
sys.setrecursionlimit(10**7)
# Load the input data from the specified file path
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read and sort input data into a grid
with open(D12_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_list: list[str]) -> list[tuple]:
    spring_list = []
    for line in input_list:
        springs, damaged_groups = line.split(' ')
        damaged_sizes = tuple(map(int, damaged_groups.split(',')))
        spring_list.append((springs, damaged_sizes))
    return spring_list

@functools.lru_cache(maxsize=None)
def count_spring_arrangements(spring_record: str, group_sizes: tuple) -> int:
    """
    Calculate the number of valid spring arrangements given a spring record and group sizes.
    """
    # If no group sizes are left, validate the spring record.
    if not group_sizes:
        return 1 if "#" not in spring_record else 0

    # If no spring record is left but there are group sizes, it's invalid.
    if not spring_record:
        return 0

    # Extract the next character from the spring record and the next group size.
    current_char = spring_record[0]
    current_group_size = group_sizes[0]

    def handle_pound():
        """Handle the case where the first character is treated as '#'."""
        # Extract and process the first group from the spring record.
        current_group = spring_record[:current_group_size].replace("?", "#")

        # If the extracted group doesn't match the expected pattern, it's invalid.
        if current_group != "#" * current_group_size:
            return 0

        # If the entire spring record matches the last group, validate the groups.
        if len(spring_record) == current_group_size:
            return 1 if len(group_sizes) == 1 else 0

        # Check if the next character after the group can be a separator.
        if spring_record[current_group_size] in "?.":
            return count_spring_arrangements(spring_record[current_group_size + 1:], group_sizes[1:])

        # Otherwise, the arrangement is invalid.
        return 0

    def handle_dot():
        """Handle the case where the first character is treated as '.'."""
        return count_spring_arrangements(spring_record[1:], group_sizes)

    # Determine the logic to apply based on the current character.
    if current_char == '#':
        result = handle_pound()
    elif current_char == '.':
        result = handle_dot()
    elif current_char == '?':
        # Explore both possibilities when the character is '?'.
        result = handle_dot() + handle_pound()
    else:
        raise ValueError("Invalid character in spring record.")

    return result

def unfold_springs(init_springs: str, init_order: tuple, expand_len: int) -> tuple[str, tuple]:
    new_springs = ((init_springs + '?') * (expand_len - 1)) + init_springs
    new_order = tuple(list(init_order) * expand_len)
    return new_springs, new_order

spring_list = parse_input(input_data)

combos_p1, combos_p2 = 0, 0
for init_springs, init_order in spring_list[:]:
    combos_p1 += count_spring_arrangements(init_springs, init_order)
    full_springs, full_order = unfold_springs(init_springs, init_order, expand_len=5)
    combos_p2 += count_spring_arrangements(full_springs, full_order)

print("Part 1:", combos_p1)
print("Part 2:", combos_p2)

# print(time.time() - start_time)