"""Advent of Code - Day 3, Year 2023
Solution Started: Dec 19, 2024
Puzzle Link: https://adventofcode.com/2023/day/3
Solution by: abbasmoosajee07
Brief: [Find numbers on a grid]
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

def parse_grid(input_list: list) -> tuple[list, dict, dict]:
    input_grid = np.array([list(row) for row in input_list], dtype=object)
    number_pos = {}
    operations = {}
    checked = set()

    for row_no, row in enumerate(input_grid):
        for col_no, char in enumerate(row):
            position = (row_no, col_no)
            if position in checked:
                continue

            checked.add(position)

            if not char.isalnum() and char != '.':
                # Store operations (non-alphanumeric and not '.')
                operations[position] = char

            elif char.isdigit():
                # Find the full number
                number_str = char
                number_positions = {position}
                current_pos = position

                # Move to the right to find the complete number
                while True:
                    next_row, next_col = current_pos[0], current_pos[1] + 1
                    if next_col < len(row) and input_grid[next_row, next_col].isdigit():
                        number_positions.add((next_row, next_col))
                        number_str += input_grid[next_row, next_col]
                        current_pos = (next_row, next_col)
                        checked.add(current_pos)  # Mark the position as checked
                    else:
                        break

                # Store the number and its positions
                number_pos[frozenset(number_positions)] = int(number_str)

    return input_grid, number_pos, operations

def get_neighbours(current_pos: tuple) -> set:
    DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1),  # up, right, down, left
                    (-1, 1), (1, 1), (1, -1), (-1, -1)]  # up-right, down-right, down-left, up-left
    row_no, col_no = current_pos
    neighbours = set()
    for dr, dc in DIRECTIONS:
        next_row, next_col = row_no + dr, col_no + dc
        # Check if the next position is within grid bounds
        if 0 <= next_row < TOTAL_ROWS and 0 <= next_col < TOTAL_COLS:
            neighbours.add((next_row, next_col))
    return neighbours  # Return neigjbours found

def find_part_numbers(number_dict: dict, operations: dict) -> int:
    total_parts = 0
    all_operations = set(operations.keys())
    for key, number in number_dict.items():
        for position in key:
            neighbours = get_neighbours(position)
            nearby_operation = neighbours & all_operations
            if len(nearby_operation) == 1:
                total_parts += number
                break
    return total_parts

def calc_gear_ratios(number_dict: dict, operations: dict, target_operations = ['*']) -> int:
    gear_ratios = 0
    for key, operation in operations.items():
        op_gear = []
        if operation in target_operations:
            op_neighbours = get_neighbours(key)
            for key, number in number_dict.items():
                nearby = key & op_neighbours
                if len(nearby) >= 1:
                    op_gear.append(number)
            if len(op_gear) == 2:
                gear_ratios += (op_gear[0] * op_gear[1])
    return gear_ratios

schematic_grid, number_dict, operations = parse_grid(input_data)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1),  # up, right, down, left
                (-1, 1), (1, 1), (1, -1), (-1, -1)]  # up-right, down-right, down-left, up-left
TOTAL_ROWS, TOTAL_COLS = len(schematic_grid), len(schematic_grid[0])


all_parts = find_part_numbers(number_dict, operations)
print("Part 1:", all_parts)

gear_ratios = calc_gear_ratios(number_dict, operations)
print("Part 2:", gear_ratios)