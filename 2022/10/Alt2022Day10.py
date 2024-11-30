"""Advent of Code - Day 10, Year 2022
Solution Started: Nov 30, 2024
Puzzle Link: https://adventofcode.com/2022/day/10
Solution by: abbasmoosajee07
Brief: [Console computer]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read and sort input data into a grid
with open(D10_file_path) as file:
    input_data = file.read().strip().split('\n')

def run_program(instructions, registers):
    cycle = 0
    signal_strength = {}
    for command in instructions:
        command = command.split(' ')
        if command[0] == 'noop':
            cycle += 1
            signal_strength[cycle] = registers['x']
        elif command[0] == 'addx':
            cycle += 1
            signal_strength[cycle] = registers['x']
            cycle += 1
            signal_strength[cycle] = registers['x']
            registers['x'] += int(command[1])
    return signal_strength

signal_strength = run_program(input_data, {'x': 1})

# List of indices to compute the strength
indices = [20, 60, 100, 140, 180, 220]

# Efficient computation using a loop and sum
ans_p1 = sum(index * signal_strength[index] for index in indices)

print("Part 1:", ans_p1)

def create_picture(signal_dict, size=(6, 40)):
    """
    Create the CRT screen for Day 10 Part 2.

    Args:
        signal_dict (dict): Dictionary with cycle as key and signal (sprite center) as value.
        size (tuple): Dimensions of the CRT screen as (rows, cols).

    Returns:
        list: A 2D array representing the CRT screen with '#' and '.'.
    """
    rows, cols = size
    crt_screen = []  # Initialize the screen

    for cycle in range(rows * cols):
        row = cycle // cols  # Determine the row for this cycle
        col = cycle % cols   # Determine the column for this cycle

        # Get the sprite's center position for the current cycle
        sprite_center = signal_dict.get(cycle + 1, 0)  # Add 1 to cycle for correct alignment

        # Determine valid positions for the sprite (sprite can be at p-1, p, or p+1)
        if col in {sprite_center - 1, sprite_center, sprite_center + 1}:
            crt_screen.append('|')  # The pixel is lit
        else:
            crt_screen.append(' ')  # The pixel is dark

    # Reshape the screen into rows and columns
    return [crt_screen[i:i + cols] for i in range(0, len(crt_screen), cols)]

message = create_picture(signal_strength)
print("Part 2:________________________________")
for row in message:
    print(''.join(row))
