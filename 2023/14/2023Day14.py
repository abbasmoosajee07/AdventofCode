"""Advent of Code - Day 14, Year 2023
Solution Started: Jan 2, 2025
Puzzle Link: https://adventofcode.com/2023/day/14
Solution by: abbasmoosajee07
Brief: [Tilting Platform]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()
# Load the input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

# Read and sort input data into a grid
with open(D14_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(init_grid: list) -> tuple[dict, tuple]:
    grid_dict = {}

    # Initialize boundaries with extreme values
    min_row, max_row = float('inf'), -float('inf')
    min_col, max_col = float('inf'), -float('inf')

    # Iterate through the grid to update each tile to dict and update bounds
    for row_no, row in enumerate(init_grid):
        for col_no, space in enumerate(row):
            if space != '.':
                if space not in grid_dict:
                    grid_dict[space] = set()
                grid_dict[space].add((row_no, col_no))

            # Update the boundaries
            min_row = min(min_row, row_no)
            max_row = max(max_row, row_no)
            min_col = min(min_col, col_no)
            max_col = max(max_col, col_no)

    # Define the space bounds
    grid_bounds = (min_row, max_row + 1, min_col, max_col + 1)

    return grid_dict, grid_bounds

def print_grid(grid_dict: dict, grid_bounds: tuple):
    min_row, max_row, min_col, max_col = grid_bounds
    grid_list = []

    for row_no in range(min_row, max_row):
        row = ''
        for col_no in range(min_col, max_col):
            pos = (row_no, col_no)
            found = False
            for key, positions in grid_dict.items():
                if pos in positions:
                    row += key
                    found = True
                    break
            if not found:
                row += '.'
        grid_list.append(row)

    for row in grid_list:
        print(row)

def calculate_load(grid_dict: dict) -> int:
    total_load = 0
    load_dict = {}

    # Find the maximum row index to adjust for reversed logic
    max_row = max(row for positions in grid_dict.values() for row, _ in positions)

    for positions in grid_dict.get('O', set()):
        row, _ = positions
        # Calculate the reversed row index
        reversed_row = max_row - row

        # Update the load dictionary with the reversed row index
        if (reversed_row + 1) not in load_dict:
            load_dict[reversed_row + 1] = 1
        else:
            load_dict[reversed_row + 1] += 1

    # Calculate the total load
    for row_index, count in load_dict.items():
        total_load += row_index * count

    return total_load

def tilt_platform(platform: dict, boundaries: tuple, tilt_dir: str):
    def get_connected_blocks() -> tuple[set, tuple]:
        connected_blocks = set()
        next_row, next_col = block_row, block_col
        connected_blocks.add((next_row, next_col))
        while True:
            next_row += dr
            next_col += dc
            if (min_row <= next_row <= max_row) and (min_col <= next_col <= max_col):
                break_point = (next_row, next_col)
                if (next_row, next_col) in fixed_blocks:
                    break_point = (next_row - dr, next_col - dc)
                    break
                elif (next_row, next_col) in moveable_blocks:
                    connected_blocks.add((next_row, next_col))
            else:
                if dc == 0:
                    base_col = next_col
                    if dr == -1:
                        base_row = min_row
                    elif dr == 1:
                        base_row = max_row - 1
                if dr == 0:
                    base_row = next_row
                    if dc == -1:
                        base_col = min_col
                    elif dc == 1:
                        base_col = max_col - 1
                break_point = (base_row, base_col)
                break
        return connected_blocks, break_point

    DIRECTIONS = {
        'North': (-1, 0),       # Move up
        'South': (1, 0),        # Move down
        'East': (0, 1),         # Move right
        'West': (0, -1),        # Move left
    }
    tilt_coords = DIRECTIONS[tilt_dir]
    dr, dc = tilt_coords
    min_row, max_row, min_col, max_col = boundaries
    fixed_blocks = set(platform.get('#', set()))
    moveable_blocks = set(platform.get('O', set()))
    tilted_blocks = set()

    while moveable_blocks:
        # Find the "last" block based on tuple comparison
        if dr == -1 or dc == -1:
            block_row, block_col = max(moveable_blocks)
        elif dr == 1 or dc == 1:
            block_row, block_col = min(moveable_blocks)
        connected_blocks, break_point = get_connected_blocks()
        final_row, final_col = break_point

        for step in range(len(connected_blocks)):
            tilted_row = final_row - (step * dr)
            tilted_col = final_col - (step * dc)
            tilted_blocks.add((tilted_row, tilted_col))
        moveable_blocks.difference_update(connected_blocks)  # Remove it from the set

    if len(platform['O']) != len(tilted_blocks):
        raise ValueError('Initial number of blocks do NOT match final number of blocks')

    final_platform = {'#': fixed_blocks, 'O': tilted_blocks}
    return final_platform

def tilt_cycle(init_platform: dict, boundaries: tuple) -> dict:
    SPIN_CYCLE = ['North', 'West', 'South', 'East']
    tilted_loads = []
    tilted_platform = copy.deepcopy(init_platform)
    for tilt_dir in SPIN_CYCLE:
        tilted_platform = tilt_platform(tilted_platform, boundaries, tilt_dir)
        tilted_loads.append(calculate_load(tilted_platform))
        # print("Tilt Direction:", tilt_dir)
        # print_grid(tilted_platform, boundaries)
    return tilted_platform, tuple(tilted_loads)

def find_cycle_for_target(tilted_platform: dict, bounds: tuple, total_cycles: int = 100) -> dict:
    load_cycles = {}
    repeating_start = None
    repeating_length = None
    target_cycle = total_cycles - 1

    for cycle in range(target_cycle):
        # Simulate the next cycle
        tilted_platform, cycle_load = tilt_cycle(tilted_platform, bounds)
        # print(f"{cycle=} {cycle_load=}") # Print for manual cycle detection

        # Check if cycle_load is repeating
        if cycle_load in load_cycles:
            repeating_start = load_cycles[cycle_load]
            repeating_length = cycle - repeating_start
            break
        load_cycles[cycle_load] = cycle

    # If no repetition found, target cycle is beyond simulation
    if repeating_start is None:
        return f"Repetition not detected within {target_cycle} cycles."

    # Map the target cycle to the repeating pattern
    if target_cycle < repeating_start:
        return f"Cycle {target_cycle} has not entered the repeating pattern."

    # Use modular arithmetic to find the equivalent cycle
    equivalent_cycle = repeating_start + (target_cycle - repeating_start) % repeating_length

    # Find the cycle_load for the equivalent cycle
    for load, cycle_num in load_cycles.items():
        if cycle_num == equivalent_cycle:
            print("Part 2:", load[-1])

            return {
                "target_cycle": target_cycle,
                "repeating_start": repeating_start,
                "repeating_length": repeating_length,
                "equivalent_cycle": equivalent_cycle,
                "cycle_load": load
            }


test_input = ['O....#....', 'O.OO#....#', '.....##...', 'OO.#O....O', '.O.....O#.', 'O.#..O.#.#', '..O..#O..O', '.......O..', '#....###..', '#OO..#....']
test_score = ['OOOO.#.O..', 'OO..#....#', 'OO..O##..O', 'O..#.OO...', '........#.', '..#....#.#', '..O..#.O.O', '..O.......', '#....###..', '#....#....']

init_platform, bounds = parse_input(input_data)

tilted_platform = tilt_platform(init_platform, bounds, 'North')
load_p1 = calculate_load(tilted_platform)
print("Part 1:", load_p1)

TOTAL_CYCLES = 1_000_000_000
target_cycle = find_cycle_for_target(init_platform, bounds, TOTAL_CYCLES)

print(f"Execution Time = {time.time() - start_time:.5f}s")

