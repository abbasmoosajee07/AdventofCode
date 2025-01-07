"""Advent of Code - Day 16, Year 2023
Solution Started: Jan 4, 2025
Puzzle Link: https://adventofcode.com/2023/day/16
Solution by: abbasmoosajee07
Brief: [Light, Mirrors and Splitters]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.setrecursionlimit(10**7)

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
                    row += movements[pos][0]
            else:
                row += '.'

        grid_list.append(row)

    # Print grid
    print("\nCurrent Grid:")
    for row in grid_list:
        print("".join(row))
    print()

def map_light_path(grid_dict: dict, light_path: dict, grid_bounds: tuple) -> dict:
    DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '>': (0, 1), '<': (0, -1)}

    SPLITTERS_MIRRORS = {  # Dictionary of how light is reflected at each mirror
        '|': {'>': 'v^', '<': 'v^', 'v': 'v', '^': '^'},
        '-': {'v': '<>', '^': '<>', '>': '>', '<': '<'},
        '\\': {'>': 'v', '^': '<', 'v': '>', '<': '^'},
        '/': {'>': '^', '^': '>', 'v': '<', '<': 'v'}
    }

    def get_next_point(init_pos, direction):
        """Calculate the next position based on direction."""
        init_row, init_col = init_pos
        dr, dc = DIRECTIONS[direction]
        next_row, next_col = init_row + dr, init_col + dc
        if MIN_ROW <= next_row < MAX_ROW and MIN_COL <= next_col < MAX_COL:
            return (next_row, next_col)
        return None

    def process_contraption(light_pos, contraption, current_direction):
        """Handle the change in light direction due to contraptions."""
        if contraption in SPLITTERS_MIRRORS:
            light_changes = SPLITTERS_MIRRORS[contraption][current_direction]
            # print(f"Contraption at {light_pos} (type: {contraption}) reflects light moving {current_direction} as: {light_changes}")
            for new_dir in light_changes:
                reflected_pos = get_next_point(light_pos, new_dir)
                if reflected_pos:
                    if reflected_pos not in light_path:
                        track_lights.append(reflected_pos)
                        light_path[reflected_pos] = [new_dir]
                        # print(f"  New light path: {reflected_pos} -> {new_dir}")
                        # print_grid(grid_dict, grid_bounds, light_path)
                    else:
                        if new_dir not in light_path[reflected_pos]:
                            light_path[reflected_pos].append(new_dir)
                            track_lights.append(reflected_pos)
                            # print(f"  Updated light path at {reflected_pos}: {light_path[reflected_pos]}")
                            # print_grid(grid_dict, grid_bounds, light_path)

    MIN_ROW, MAX_ROW, MIN_COL, MAX_COL = grid_bounds
    track_lights = list(light_path.keys())

    # Ensure light directions are stored as lists for consistency
    for key in light_path:
        light_path[key] = [light_path[key]]

    while track_lights:
        # Get the current position and direction
        light_pos = track_lights.pop()
        current_directions = light_path[light_pos]

        # Process each direction for the current light position
        for current_direction in current_directions:
            # print(f"Tracking light at {light_pos}, moving {current_direction}")

            # Check for contraptions (splitters or mirrors) at the current location
            if light_pos in grid_dict:
                contraption = grid_dict[light_pos]
                # print(f"  Found contraption at {light_pos}: {contraption}")
                process_contraption(light_pos, contraption, current_direction)
            else:
                # No contraption, just move the light in the current direction
                next_loc = get_next_point(light_pos, current_direction)
                if next_loc:
                    if next_loc not in light_path:
                        light_path[next_loc] = [current_direction]
                        track_lights.append(next_loc)
                        # print(f"  No contraption, moving to next position: {next_loc} with direction {current_direction}")
                    elif current_direction not in light_path[next_loc]:
                        light_path[next_loc].append(current_direction)
                        track_lights.append(next_loc)
                        # print(f"  Updated light path at {next_loc}: {light_path[next_loc]}")

    return light_path

def maximise_light_energy(grid_dict: dict, grid_bounds: tuple) -> int:
    min_row, max_row, min_col, max_col = grid_bounds
    light_directions = ['>', '<', 'v', '^']
    max_energy = 0
    max_coords = []

    borders = set()

    # Add top and bottom rows
    for col_no in range(min_col, max_col):
        borders.add((min_row, col_no))
        borders.add((max_row - 1, col_no))

    # Add left and right columns
    for row_no in range(min_row, max_row):
        borders.add((row_no, min_col))
        borders.add((row_no, max_col - 1))

    for border_coords in borders:
        for test_dir in light_directions:
            test_movements = map_light_path(grid_dict, {border_coords:test_dir}, bounds)
            if  len(test_movements) >= max_energy:
                max_energy = len(test_movements)
                max_coords.append((border_coords,test_dir))
    return max_energy, max_coords

grid_dict, bounds = parse_grid(input_data)
movement_dict = map_light_path(grid_dict, {(0,0):'>'}, bounds)
print("Part 1:", len(movement_dict))

max_energy = maximise_light_energy(grid_dict, bounds)
print("Part 2:", max_energy[0])

print(f"Execution Time = {time.time() - start_time:.5f}s")
