"""Advent of Code - Day 9, Year 2023
Solution Started: Dec 26, 2024
Puzzle Link: https://adventofcode.com/2023/day/9
Solution by: abbasmoosajee07
Brief: [Extrapolating Numbers in Sequences]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()
# Load the input data from the specified file path
D09_file = "Day09_input.txt"
D09_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D09_file)

# Read and sort input data into a grid
with open(D09_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_seq: list[str]) -> list[int]:
    return [list(map(int, row.split(' '))) for row in input_seq]

def print_triangle(data: list[list[str]]):
    # Determine the maximum width needed for the numbers
    max_number = max(max(row) for row in data if row)  # Find the largest number
    number_width = len(str(max_number))  # Determine the width of the largest number
    spacer = ' ' * (number_width + 1)  # Standard space between numbers

    # Create a function to center a number within its gap
    def center(num):
        return f"{num:^{number_width}}"

    for i, row in enumerate(data):
        # For subsequent rows, calculate the alignment
        leading_spaces = spacer * i
        row_content = spacer.join(center(num) for num in row)
        print(f"{leading_spaces}{row_content}")

def calculate_diffs(seq: list[int]) -> list[int]:
    """Helper function to calculate differences between consecutive numbers."""
    return [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]

def build_number_history(number_sequence: list[int]) -> list[list[int]]:

    full_history = [number_sequence]

    while True:
        # Check if the sequence is all zeros or has only one number
        if all(x == 0 for x in number_sequence) or len(number_sequence) == 1:
            break

        # Calculate differences and append to history
        diffs = calculate_diffs(number_sequence)
        full_history.append(diffs)

        # Update sequence for the next iteration
        number_sequence = diffs

    return full_history

def extrapolate_forward(number_history: list[list[int]]) -> tuple[list[list[int]], int]:
    final_value = 0
    use_history = copy.deepcopy(number_history[::-1])  # Reverse the history
    updated_history = []

    for seq_no, seq in enumerate(use_history[:-1]):
        # Calculate new value by adding the last value of the current and next sequence
        new_val = seq[-1] + use_history[seq_no + 1][-1]

        # Update the current sequence and append the new value to the next sequence
        use_history[seq_no + 1].append(new_val)  # Modify in place

        # Keep track of the updated history
        updated_history.append(use_history[seq_no + 1])

        # Set final value to the new value
        final_value = new_val

    # Return the updated history and the final value
    return updated_history[::-1], final_value

def extrapolate_backwards(number_history: list[list[int]]) -> tuple[list[list[int]], int]:
    final_value = 0
    use_history = copy.deepcopy(number_history[::-1])  # Reverse the history and deep copy
    updated_history = []

    # Start with the first sequence (after reversal, it's the last sequence)
    use_history[0].insert(0, 0)  # Insert 0 at the start of the first sequence
    updated_history.append(use_history[0])  # Add the modified first sequence to updated history
    
    for seq_no in range(1, len(use_history)):  # Start from the second sequence
        # Calculate new value by adding the first value of the current and next sequence
        new_val = use_history[seq_no][0] - use_history[seq_no - 1][0]

        # Insert the new value at the start of the current sequence
        use_history[seq_no].insert(0, new_val)

        # Keep track of the updated history
        updated_history.append(use_history[seq_no])

        # Set final value to the new value
        final_value = new_val

    # Reverse the updated history to restore original order
    return updated_history[::-1], final_value


test_input = ['0 3 6 9 12 15', '1 3 6 10 15 21', '10 13 16 21 30 45']
number_seq = parse_input(input_data)

forward_sum, backward_sum = 0, 0
for seq_no, sequence in enumerate(number_seq[:]):
    num_history = build_number_history(sequence)
    forward_history, forward_value = extrapolate_forward(num_history)
    forward_sum += forward_value
    back_history, backward_value = extrapolate_backwards(num_history)
    backward_sum += backward_value
    # print(f"{seq_no=} {forward_value=} {backward_value=}")
    # print_triangle(num_history)
    # print_triangle(back_history)

print("Part 1:", forward_sum)
print("Part 2:", backward_sum)
print(time.time() - start_time)