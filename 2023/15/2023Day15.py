"""Advent of Code - Day 15, Year 2023
Solution Started: Jan 3, 2025
Puzzle Link: https://adventofcode.com/2023/day/15
Solution by: abbasmoosajee07
Brief: [Coded and arranging lens]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split(',')

def decode_hash(coded_string: str, decoded_value: int = 0) -> int:
    def HASH_algorithm(char: str, init_value: int) -> int:
        # Calculate the ASCII value of the character
        ascii_value = ord(char)
        # Apply the hash transformation
        return (ascii_value + init_value) * 17 % 256

    # Apply the HASH_algorithm to each character in the coded string
    for character in coded_string:
        decoded_value = HASH_algorithm(character, decoded_value)
    return decoded_value

def sort_lens(lens_list: list[str]) -> tuple[dict, int]:
    """Sort lens into boxes from 0 to 255"""
    boxes_dict = {box_no: [] for box_no in range(256)}  # Initialize empty boxes
    lens_sum = 0

    for lens in lens_list:
        if '=' in lens:
            label, value = lens.split('=')
            value = int(value)
            operation = '='
        elif '-' in lens:
            label, value = lens.strip('-'), None
            operation = '-'
        else:
            continue

        decoded_lens = decode_hash(label)

        if operation == '=':
            # Replace existing label or append if not found
            for i, (existing_label, _) in enumerate(boxes_dict[decoded_lens]):
                if existing_label == label:
                    boxes_dict[decoded_lens][i] = (label, value)
                    break
            else:
                boxes_dict[decoded_lens].append((label, value))

        elif operation == '-':
            # Remove label if found
            boxes_dict[decoded_lens] = [
                (existing_label, existing_value)
                for existing_label, existing_value in boxes_dict[decoded_lens]
                if existing_label != label
            ]
        # Debugging output
        # print(f"\n Add {lens}")
        # for box_no, box_set in boxes_dict.items():
        #     if box_set:  # Print only non-empty boxes
        #         print("Box", box_no, box_set)

    # Calculate lens_sum
    for box_no, box_set in boxes_dict.items():
        for lens_idx, (lens, focal) in enumerate(box_set, start=1):
            if focal is not None:
                lens_sum += (box_no + 1) * lens_idx * focal

    return boxes_dict, lens_sum

code_sum = sum(decode_hash(code) for code in input_data)
print("Part 1:", code_sum)

boxes, lens_sum = sort_lens(input_data)
print("Part 2:", lens_sum)
