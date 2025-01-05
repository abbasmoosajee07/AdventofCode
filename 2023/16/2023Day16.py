"""Advent of Code - Day 16, Year 2023
Solution Started: Jan 4, 2025
Puzzle Link: https://adventofcode.com/2023/day/16
Solution by: abbasmoosajee07
Brief: [Light, Mirrors and Splitters]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_grid(init_grid: list) -> tuple[dict, tuple]:
    grid_dict = {}

    # Initialize boundaries with extreme values
    min_row, max_row = float('inf'), -float('inf')
    min_col, max_col = float('inf'), -float('inf')

    # Iterate through the grid to update each tile to dict and update bounds
    for row_no, row in enumerate(init_grid):
        for col_no, tile in enumerate(row):
            if tile != '.':
                grid_dict[(row_no, col_no)] = tile

            # Update the boundaries
            min_row = min(min_row, row_no)
            max_row = max(max_row, row_no)
            min_col = min(min_col, col_no)
            max_col = max(max_col, col_no)

    # Define the space bounds
    grid_bounds = (min_row, max_row + 1, min_col, max_col + 1)

    return grid_dict, grid_bounds

def print_grid(grid_dict: dict, grid_bounds: tuple, movements: dict):
    min_row, max_row, min_col, max_col = grid_bounds
    grid_list = []

    for row_no in range(min_row, max_row):
        row = ''
        for col_no in range(min_col, max_col):
            pos = (row_no, col_no)
            if pos in grid_dict.keys():
                row += grid_dict[pos]
            elif pos in movements.keys():
                if len(movements[pos]) >= 2:
                    row += str(len(movements[pos]))
                else:
                    row += movements[pos]
            else:
                row += '.'
        grid_list.append(row)

    for row in grid_list:
        print(row)

def map_light_path(grid_dict: dict, light_path: dict, grid_bounds: tuple) -> dict:
    DIRECTIONS = {'^':(-1,0), 'v':(1,0), '>':(0,1), '<':(0,-1)}

    SPLITTERS_MIRRORS = { # Dictionary of how light is reflected at each mirror
        '|': {'>': 'v^', '<': 'v^', 'v': 'v', '^': '^'},
        '-': {'v': '<>', '^': '<>', '>': '>', '<': '<'},
        '\\' : {'>':'v', '^':'<', 'v':'>', '<':'^'},
        '/'  : {'>':'^', '^':'>', 'v':'<', '<':'v'}
    }

    def get_next_point(init_pos, direction):
        init_row, init_col = init_pos
        dr, dc = DIRECTIONS[direction]
        next_row, next_col = init_row + dr, init_col + dc
        if MIN_ROW <= next_row <= MAX_ROW and MIN_COL <= next_col <= MAX_COL:
            return (next_row, next_col)
        return None

    MIN_ROW, MAX_ROW, MIN_COL, MAX_COL = grid_bounds
    track_lights = list(light_path.keys())
    path_history = {}
    while track_lights:
        # Get the current position and direction
        light_pos = track_lights.pop()
        current_direction = light_path[light_pos]
        # Get the next position
        print(f"{light_pos=}, {current_direction=}")

        # Check for contraptions (splitters or mirrors) at the next location
        if light_pos in grid_dict:
            contraption = grid_dict[light_pos]
            if contraption in SPLITTERS_MIRRORS:
                light_changes = SPLITTERS_MIRRORS[contraption][current_direction]
                print(f"{light_pos=} {current_direction=} {contraption=} {light_changes=}")
                for new_dir in light_changes:
                    reflected_pos = get_next_point(light_pos, new_dir)
                    if reflected_pos:
                        if reflected_pos not in light_path.keys():
                            track_lights.append(reflected_pos)
                            light_path[reflected_pos] = new_dir
                            path_history[light_pos] = [(reflected_pos, new_dir)]
                            print(f"{current_direction=} {contraption=} {new_dir=} {reflected_pos=}")
                            print_grid(grid_dict, grid_bounds, light_path)
                        else:
                            print(new_dir, reflected_pos, light_path[reflected_pos])
                            light_path[reflected_pos] = new_dir

        # Update light path and add the next location to be tracked
        else:
            next_loc = get_next_point(light_pos, current_direction)
            if next_loc:
                light_path[next_loc] = current_direction
                track_lights.append(next_loc)

    return light_path

test_input = ['.|...\\....', '|.-.\\.....', '.....|-...', '........|.', '..........', '.........\\', '..../.\\\\..', '.-.-/..|..', '.|....-|.\\', '..//.|....']

grid_dict, bounds = parse_grid(test_input)
movement_dict = map_light_path(grid_dict, {(0,0):'>'}, bounds)
print(movement_dict)
# print_grid(grid_dict, bounds, movement_dict)
print("Part 1:", len(movement_dict))
print(f"Execution Time = {time.time() - start_time:.5f}s")

# >|<<<\....
# |v-.\^....
# .v...|->>>
# .v...v^.|.
# .v...v^...
# .v...v^..\
# .v../2\\..
# <->-/vv|..
# .|<<<2-|.\
# .v//.|.v..

