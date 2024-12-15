"""Advent of Code - Day 15, Year 2024
Solution Started: Dec 15, 2024
Puzzle Link: https://adventofcode.com/2024/day/15
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
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
    grid_map  = np.array([list(row) for row in map_input], dtype=object)
    total_rows, total_cols = len(grid_map), len(grid_map[0])
    empty_map = [['.' for _ in range(total_cols)] for _ in range(total_rows)]
    box_count = 0

    # Assuming start and end is on the border
    for row_index, row in enumerate(grid_map):
        for col_index, cell in enumerate(row):
            if grid_map[row_index][col_index] == '#':
                empty_map[row_index][col_index] = grid_map[row_index][col_index]
            if cell == '@':
                robot = (row_index, col_index)
            if cell == 'O':
                box_count += 1


    return empty_map, grid_map, movements, box_count, robot

def calculate_box_GPS(map):
    gps_sum = 0
    for row_no, row in enumerate(map):
        for col_no, char in enumerate(row):
            if char == 'O':
                box_gps = (100 * row_no) + col_no
                # print(f"{row_no=}, {col_no=}, {box_gps=}")
                gps_sum += box_gps
    return gps_sum

def move_robot(map, movement, robot_start):

    def move_boxes(map, robot_pos, dr, dc):
            new_map = copy.deepcopy(map)
            robot_stop = (robot_pos[0] + dr, robot_pos[1] + dc)
            box_list = []

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
                    if char == 'O':
                        box_list.append((target_idx, col_idx))
                    elif char in ['#', '@', 'O']:
                        break
                    else:
                        break

            elif dc == 0 and abs(dr) == 1:  # Vertical movement
                target_idx = robot_pos[1]
                target_col = [row[target_idx] for row in map]
                if dr == 1:
                    col_end = len(target_col)
                elif dr == -1:
                    col_end = 0
                for row_idx in range(robot_pos[0] + dr, col_end, dr):
                    char = target_col[row_idx]
                    if char == 'O':
                        box_list.append((row_idx, target_idx))
                    elif char in ['#', '@', 'O']:
                        break
                    else:
                        break

            # Check if the last box can move
            if box_list:
                last_row, last_col = box_list[-1]
                next_row, next_col = last_row + dr, last_col + dc

                if not (0 <= next_row < len(map) and 0 <= next_col < len(map[0])):
                    return new_map, robot_pos  # Path is out of bounds

                if map[next_row][next_col] != '.':
                    return new_map, robot_pos  # Path is blocked

                # Move boxes
                for box_row, box_col in reversed(box_list):
                    new_map[box_row + dr][box_col + dc] = 'O'  # Move box forward
                    new_map[box_row][box_col] = '.'  # Clear old box position

            # Update robot position
            new_map[robot_pos[0]][robot_pos[1]] = '.'  # Clear old position
            new_map[robot_stop[0]][robot_stop[1]] = '@'  # Move robot to the new position

            return new_map, robot_stop

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
        elif map[new_row][new_col] == 'O':  # Special action on obstacle
            new_map, robot_stop = move_boxes(map, robot_start, dr, dc)
            return new_map, robot_stop  # Reset to empty map

    # Return the unchanged map and position if the move is invalid
    return map, robot_start

test_input_1 = ['########\n#..O.O.#\n##@.O..#\n#...O..#\n#.#.O..#\n#...O..#\n#......#\n########', '<^^>>>vv<v>>v<<']

test_input_2 = ['##########\n#..O..O.O#\n#......O.#\n#.OO..O.O#\n#..O@..O.#\n#O#..O...#\n#O..O..O.#\n#.OO.O.OO#\n#....O...#\n##########',
                '<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^\nvvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v\n><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<\n<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^\n^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><\n^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^\n>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^\n<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>\n^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>\nv^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^']

EMPTY_MAP, past_map, movement_list, BOX_COUNT, robot_previous = parse_input(input_data)

# Iterate through the movement list
for movement in movement_list[:]:
    # Move the robot and get the updated map and position
    past_map, robot_previous = move_robot(past_map, movement, robot_previous)

    # Display the movement and updated map
    # print(f"Movement: {movement}")
    # for row in past_map:
    #     print(''.join(row))


ans_p1 = calculate_box_GPS(past_map)
print("Part 1:", ans_p1)

##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########
