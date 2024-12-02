"""Advent of Code - Day 13, Year 2022
Solution Started: Dec 1, 2024
Puzzle Link: https://adventofcode.com/2022/day/13
Solution by: abbasmoosajee07
Brief: [Lists and Recursion]
"""

#!/usr/bin/env python3

import os, re, copy, ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functools import cmp_to_key

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

with open(D13_file_path) as file:
    input_data = file.read().strip().split('\n\n')

# Function to compare two lists recursively
def compare_list_elements(left_list, right_list):
    if len(left_list) and len(right_list):
        # Compare the first elements, and recursively compare the rest if needed
        comparison_result = compare_elements(left_list[0], right_list[0])
        return comparison_result if comparison_result != 0 else compare_list_elements(left_list[1:], right_list[1:])
    # If one list is shorter, return the comparison of their lengths
    return (len(left_list) > len(right_list)) - (len(left_list) < len(right_list))

# Function to compare two elements, handling both integers and lists
def compare_elements(left_element, right_element):
    left_type, right_type = type(left_element), type(right_element)

    # If both are integers, compare them
    if left_type == int and right_type == int:
        return (left_element > right_element) - (left_element < right_element)

    # If not, convert them to lists if needed and recursively compare
    return compare_list_elements(left_element if left_type == list else [left_element],
                                    right_element if right_type == list else [right_element])

def count_valid_lists(input_lists):
    """
    Collect all valid pairs in the input and return their 1-based indices.
    """
    valid_pairs = []
    for list_no, list_pair in enumerate(input_lists):
        # Split each pair into left and right lists
        left_list, right_list = list_pair.split('\n')
        left_list = ast.literal_eval(left_list)
        right_list = ast.literal_eval(right_list)
        # Check if the pair is valid
        validity = compare_elements(left_list, right_list)
        if validity < 0:  # Assume valid means left < right
            valid_pairs.append(list_no + 1)  # Add 1 to match 1-based indexing
    return valid_pairs

# Part 1
valid_pairs = count_valid_lists(input_data)
print("Part 1:", sum(valid_pairs))

def sort_packets(input_data):
    """
    Sort all packets, including special markers [[2]] and [[6]], 
    and return the product of their positions in the sorted list.

    Args:
        input_data (list of str): List of packet pairs as newline-separated strings.

    Returns:
        int: Product of 1-based positions of [[2]] and [[6]] in the sorted list.
    """
    # Parse all lists from input_data
    parsed_lists = [
        ast.literal_eval(line)
            for lists in input_data
            for line in lists.split('\n')
    ]

    # Add special markers [[2]] and [[6]]
    packets = parsed_lists + [[[2]], [[6]]]

    # Sort the packets using compare_elements for custom comparison
    sorted_packets = sorted(packets, key=cmp_to_key(compare_elements))

    # Find 1-based positions of [[2]] and [[6]]
    pos_2 = sorted_packets.index([[2]]) + 1
    pos_6 = sorted_packets.index([[6]]) + 1

    # Return the product of the positions
    return pos_2 * pos_6

# Part 2
ans_p2 = sort_packets(input_data)
print("Part 2:", ans_p2)
