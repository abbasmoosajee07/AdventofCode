"""Advent of Code - Day 15, Year 2024
Solution Started: Dec 15, 2024
Puzzle Link: https://adventofcode.com/2024/day/15
Solution by: abbasmoosajee07
Brief: [Moving Boxes w/ Robots]
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
    input_data = file.read().strip().split('\n\n')

def parse_input(input):
    map_input = input[0].split('\n')
    movements = list(input[1].replace('\n',''))
    standard_map  = np.array([list(row) for row in map_input], dtype=object)
    total_rows, total_cols = len(standard_map), len(standard_map[0])
    extended_map = [['.' for _ in range(total_cols)] for _ in range(total_rows)]
    # Assuming start and end is on the border
    for row_index, row in enumerate(standard_map):
        for col_index, cell in enumerate(row):
            if cell == '@':
                start_p1 = (row_index, col_index)
            if cell == '#':
                extended_map[row_index][col_index] = '##'
            if cell == 'O':
                extended_map[row_index][col_index] = '[]'
            if cell == '.':
                extended_map[row_index][col_index] = '..'
            if cell == '@':
                extended_map[row_index][col_index] = '@.'
    expanded_map = np.array([list(''.join(row)) for row in extended_map], dtype=object)

    start_p2 = (start_p1[0],2*start_p1[1])
    return expanded_map, standard_map, start_p1, start_p2, movements

def calculate_box_GPS(map):
    gps_sum = 0
    for row_no, row in enumerate(map):
        for col_no, char in enumerate(row):
            if char in ['O','[']:
                box_gps = (100 * row_no) + col_no
                gps_sum += box_gps
    return gps_sum

def move_boxes(map, robot_pos, dr, dc):

    new_map = copy.deepcopy(map)
    robot_stop = (robot_pos[0] + dr, robot_pos[1] + dc)
    box_dict = {}

    # Identify the target row/column and collect boxes in the path
    if dr == 0 and abs(dc) == 1:  # Horizontal movement
        target_idx = robot_pos[0]
        target_row = map[target_idx]
        if dc == 1:
            row_end = len(target_row)
        elif dc == -1:
            row_end = 0
        for col_idx in range(robot_pos[1] + dc, row_end, dc):
            char = target_row[col_idx]
            if char in ['O','[',']']:
                box_dict[(target_idx, col_idx)] = char
            elif char in ['#', '@']:
                break
            else:
                break

    elif dc == 0 and abs(dr) == 1:  # Vertical movement
        def move_box_columns(map, box, dr):
            box_columns = {}
            row, col = box
            new_row = row + dr

            # Ensure movement is within bounds
            if 0 <= new_row < len(map):
                # Check for the trailing part of the box (`[`, `]`)
                if map[new_row][col] == ']':  # Box's right side
                    adjacent_pos = (new_row, col - 1)  # Left side of the box
                    box_columns[(new_row, col)] = map[new_row][col]
                    box_columns[adjacent_pos] = map[adjacent_pos]
                elif map[new_row][col] == '[':  # Box's left side
                    adjacent_pos = (new_row, col + 1)  # Right side of the box
                    box_columns[(new_row, col)] = map[new_row][col]
                    box_columns[adjacent_pos] = map[adjacent_pos]
                elif map[new_row][col] == 'O':  # Single box
                    box_columns[(new_row, col)] = map[new_row][col]

            return box_columns

        # Add the robot's current position and the item at that position to box_dict
        box_dict[robot_stop] = map[robot_stop[0]][robot_stop[1]]

        # Move the adjacent box and update the box dictionary
        adjacent_box = move_box_columns(map, robot_pos, dr)
        box_dict.update(adjacent_box)
        check_boxes = list(box_dict.keys())
        # print(check_boxes)
        # Process each box in box_check
        while check_boxes:  # Use a while loop since we'll dynamically modify box_check
            # Get the first box position to process
            test_box = check_boxes.pop(0)

            # Move the box in the column (the function should return updated positions for boxes)
            box_column = move_box_columns(map, test_box, dr)

            # Extend box_check with new box positions from box_column
            check_boxes.extend(box_column.keys())

            # Update the box_dict with the new positions of the boxes
            box_dict.update(box_column)

        # print(box_dict)
    # Check if the last box can move
    if box_dict:
        # Get the last box's position from the dictionary
        last_pos = list(box_dict.keys())[-1]  # Get the last key (position)
        last_row, last_col = last_pos
        next_row, next_col = last_row + dr, last_col + dc

        # Check if the next position is within bounds
        if not (0 <= next_row < len(map) and 0 <= next_col < len(map[0])):
            return new_map, robot_pos  # Path is out of bounds

        # Check if the path is blocked
        if map[next_row][next_col] != '.':
            return new_map, robot_pos  # Path is blocked

        for (box_row, box_col) in list(box_dict.keys())[::-1]:
            wall_check = map[box_row + dr][box_col + dc]
            if wall_check ==  '#':
                return new_map, robot_pos
        # Move boxes
        for (box_row, box_col) in list(box_dict.keys())[::-1]:
            new_map[box_row + dr][box_col + dc] = box_dict[(box_row,box_col)]  # Move box forward
            new_map[box_row][box_col] = '.'  # Clear old box position
        # Update robot position
        new_map[robot_pos[0]][robot_pos[1]] = '.'  # Clear old position
        new_map[robot_stop[0]][robot_stop[1]] = '@'  # Move robot to the new position

    return new_map, robot_stop

def move_robot(map, movement, robot_start):
    # Define movement directions: (row_delta, col_delta)
    DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    dr, dc = DIRECTIONS[movement]
    new_row, new_col = robot_start[0] + dr, robot_start[1] + dc

    # Check if the next position is within bounds and valid
    if 0 <= new_row < len(map) and 0 <= new_col < len(map[0]):
        if map[new_row][new_col] == '.':  # Move to empty cell
            map[new_row][new_col] = '@'  # Mark new robot position
            map[robot_start[0]][robot_start[1]] = '.'  # Clear old position
            return map, (new_row, new_col)
        elif map[new_row][new_col] in ['O','[',']']:  # Special action on obstacle
            new_map, robot_stop = move_boxes(map, robot_start, dr, dc)
            return new_map, robot_stop  # Reset to empty map

    # Return the unchanged map and position if the move is invalid
    return map, robot_start

map_p2, map_p1, robot_p1, robot_p2, movement_list = parse_input(input_data)

# Iterate through the movement list
for movement in movement_list[:]:

    # Move the robot and get the updated map and position
    map_p1, robot_p1 = move_robot(map_p1, movement, robot_p1)

    map_p2, robot_p2 = move_robot(map_p2, movement, robot_p2)

ans_p1 = calculate_box_GPS(map_p1)
print("Part 1:", ans_p1)

ans_p2 = calculate_box_GPS(map_p2)
print("Part 2:", ans_p2)
