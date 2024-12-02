"""Advent of Code - Day 14, Year 2022
Solution Started: Dec 2, 2024
Puzzle Link: https://adventofcode.com/2022/day/14
Solution by: abbasmoosajee07
Brief: [Mapping Sand Flow in a Cave]
"""

#!/usr/bin/env python3

import os, re, copy, sys, collections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.setrecursionlimit(10**9)  # Increase the recursion depth

# Load the input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

# Read and sort input data into a grid
with open(D14_file_path) as file:
    input_data = file.read().strip().split('\n')

# Read and parse the rock veins into coordinates
def create_rock_map(input):
    rocks = collections.defaultdict(bool)
    for rock_line in input:
        rock_coords = rock_line.split(' -> ')
        for idx in range(len(rock_coords) - 1):
            x1, y1 = map(int, rock_coords[idx].split(','))
            x2, y2 = map(int, rock_coords[idx + 1].split(','))
            if x1 == x2:
                x = x1
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    rocks[(x, y)] = True
            if y1 == y2:
                y = y1
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    rocks[(x, y)] = True
    return rocks

def simulate_sand(rocks, spring, cave_bottom=None):
    """
    Simulates sand flow in the cave based on rock and optional floor configurations.

    Args:
    - rocks: dict, rock map where keys are coordinates and values indicate if rock exists.
    - spring: tuple, starting position of the sand (x, y).
    - cave_bottom: int, optional, depth of the floor below the rocks.

    Returns:
    - settled_sand: set, coordinates of settled sand particles.
    """
    local_rocks = copy.deepcopy(rocks)
    settled_sand = set()
    x, y = spring

    # Determine maximum depth where sand can settle
    max_y = max(y for _, y in rocks)
    limit_y = cave_bottom if cave_bottom else max_y

    while True:
        nx, ny = x, y
        while True:
            # Stop simulation if sand flows below the maximum allowed depth
            if ny > limit_y:
                return settled_sand

            # Stop sand at the floor, if defined
            if cave_bottom and ny + 1 >= cave_bottom:
                settled_sand.add((nx, ny))
                break

            # Move down if no rock or sand is below
            if not local_rocks[(nx, ny + 1)] and (nx, ny + 1) not in settled_sand:
                ny += 1
            # Move diagonally left if possible
            elif not local_rocks[(nx - 1, ny + 1)] and (nx - 1, ny + 1) not in settled_sand:
                nx, ny = nx - 1, ny + 1
            # Move diagonally right if possible
            elif not local_rocks[(nx + 1, ny + 1)] and (nx + 1, ny + 1) not in settled_sand:
                nx, ny = nx + 1, ny + 1
            else:
                # Sand settles
                settled_sand.add((nx, ny))
                break

        # Stop if sand cannot settle anymore
        if nx == x and ny == y: # Condition for Part 2
            break

    return settled_sand

rock_coords = create_rock_map(input_data)

# Start simulation from the spring point (500, 0)
cave_opening = (500, 0)
settled_sand_p1 = simulate_sand(rock_coords, cave_opening)
print(f"Part 1: {len(settled_sand_p1)}")

floor_depth = 2
cave_bottom = max(y for _, y in rock_coords) + floor_depth
settled_sand_p2 = simulate_sand(rock_coords, cave_opening, cave_bottom)
print(f"Part 2: {len(settled_sand_p2)}")

def save_grid(rock_coords, sand, floor_depth = 0, part=1, padding=0):
    # Set grid boundaries with padding
    grid_min_x = min(min(x for x, y in rock_coords), min(x for x, y in sand)) - padding
    grid_max_x = max(max(x for x, y in rock_coords), max(x for x, y in sand)) + padding
    grid_min_y = min(min(y for x, y in rock_coords), min(y for x, y in sand)) * 0
    grid_max_y = max(max(y for x, y in rock_coords), max(y for x, y in sand)) #+ cave_bottom

    # Create a grid with the dimensions of the area
    grid_width = grid_max_x - grid_min_x + 1
    grid_height = grid_max_y - grid_min_y + 1
    grid = [['.' for _ in range(grid_width)] for _ in range(grid_height)]

    # Populate the grid with rocks
    for (x, y) in rock_coords:
        if grid_min_x <= x <= grid_max_x and grid_min_y <= y <= grid_max_y:
            grid[y - grid_min_y][x - grid_min_x] = '#'

    # Populate the grid with sand
    for (x, y) in sand:
        if grid_min_x <= x <= grid_max_x and grid_min_y <= y <= grid_max_y:
            grid[y - grid_min_y][x - grid_min_x] = 'o'

    # Populate the grid with the floor, if applicable
    if floor_depth > 0:
        for x in range(grid_min_x, grid_max_x + 1):
            if grid_min_x <= x <= grid_max_x and grid_min_y <= y <= grid_max_y:
                grid[grid_max_y][x - grid_min_x] = '-'

    # Add the sand spout
    if grid_min_x <= 500 <= grid_max_x:
        grid[0][500 - grid_min_x] = '+'

    # Save the grid to a file
    grid_file_path = f"cave_grid_p{part}.txt"
    with open(grid_file_path, 'w') as file:
        for row in grid:
            file.write("".join(row) + '\n')

    print(f"Grid saved to {grid_file_path}")


# # Call the function to save the grid
# save_grid(rock_coords, settled_sand_p1, part = 1)
# save_grid(rock_coords, settled_sand_p2, floor_depth, part = 2, padding= 5)

