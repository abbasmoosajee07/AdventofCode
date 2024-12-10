"""Advent of Code - Day 20, Year 2022
Solution Started: Dec 9, 2024
Puzzle Link: https://adventofcode.com/2022/day/20
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    input_data = file.read().strip().split('\n')
    encrypted_file = [int(num) for num in input_data]

def find_grove_coordinates(file_list, grove = [1000, 2000, 3000]):
    file = []
    file_len = len(file_list)
    zero_pos = [i for i, value in enumerate(file_list) if value == 0]

    for coordinate in grove:
        idx = (coordinate + zero_pos[0]) % file_len
        number = file_list[idx]
        file.append(number)
    return file

def mix_file(file, decryption_key = 1, mix_rounds = 1):
    """
    Mix the file based on the movement rules, accounting for duplicate values.
    """
    # Attach unique identifiers to each number to differentiate duplicates
    indexed_file = [((value * decryption_key), idx) for idx, value in enumerate(file)]
    mixed_file = copy.deepcopy(indexed_file)  # Avoid modifying the original list

    file_len = len(file)
    for round in range(mix_rounds):

        for original in indexed_file:
            move_num, original_idx = original

            # Find the current index of the specific instance in the mixed file
            idx_pos = mixed_file.index(original)

            # Calculate the new position using modular arithmetic
            new_pos = (idx_pos + move_num) % (file_len - 1)  # Wrap within list length minus 1

            # Remove the number from its current position and insert at the new position
            del mixed_file[idx_pos]
            mixed_file.insert(new_pos, original)

    # Return only the values (strip off the unique identifiers)
    return [value for value, idx in mixed_file]


mixed_p1 = mix_file(encrypted_file)
coords_p1 = find_grove_coordinates(mixed_p1)
print("Part 1:", sum(coords_p1))

mixed_p2 = mix_file(encrypted_file, decryption_key=811589153, mix_rounds=10)
coords_p2 = find_grove_coordinates(mixed_p2)
print("Part 2:", sum(coords_p2))
