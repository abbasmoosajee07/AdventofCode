# Advent of Code - Day 17, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/17
# Solution by: [abbasmoosajee07]
# Brief: [Conway Cubes]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n')

def evolve_grid_3d(active_cubes):
    for _ in range(6):  # Simulate six cycles
        next_active_cubes = set()
        x_values = [x for x, y, z in active_cubes]
        y_values = [y for x, y, z in active_cubes]
        z_values = [z for x, y, z in active_cubes]

        # Iterate over the extended bounding box
        for x in range(min(x_values) - 1, max(x_values) + 2):
            for y in range(min(y_values) - 1, max(y_values) + 2):
                for z in range(min(z_values) - 1, max(z_values) + 2):
                    active_neighbors = 0
                    # Count active neighbors
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            for dz in [-1, 0, 1]:
                                if (dx, dy, dz) != (0, 0, 0):
                                    if (x + dx, y + dy, z + dz) in active_cubes:
                                        active_neighbors += 1
                    # Apply Conway's rules
                    if (x, y, z) in active_cubes and active_neighbors in [2, 3]:
                        next_active_cubes.add((x, y, z))
                    elif (x, y, z) not in active_cubes and active_neighbors == 3:
                        next_active_cubes.add((x, y, z))

        active_cubes = next_active_cubes

    return len(active_cubes)

# Initialize active cubes for Part 1 (3D)
def parse_input_to_active_3d(input_data):
    active_cubes = set()
    for row, line in enumerate(input_data):
        for col, char in enumerate(line):
            if char == '#':
                active_cubes.add((row, col, 0))
    return active_cubes

# Solve Part 1
active_cubes_3d = parse_input_to_active_3d(input_data)
print(f'Part 1: {evolve_grid_3d(active_cubes_3d)}')

def evolve_grid_4d(active_cubes):
    for _ in range(6):  # Simulate six cycles
        next_active_cubes = set()
        x_values = [x for x, y, z, w in active_cubes]
        y_values = [y for x, y, z, w in active_cubes]
        z_values = [z for x, y, z, w in active_cubes]
        w_values = [w for x, y, z, w in active_cubes]

        # Iterate over the extended bounding box
        for x in range(min(x_values) - 1, max(x_values) + 2):
            for y in range(min(y_values) - 1, max(y_values) + 2):
                for z in range(min(z_values) - 1, max(z_values) + 2):
                    for w in range(min(w_values) - 1, max(w_values) + 2):
                        active_neighbors = 0
                        # Count active neighbors
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                for dz in [-1, 0, 1]:
                                    for dw in [-1, 0, 1]:
                                        if (dx, dy, dz, dw) != (0, 0, 0, 0):
                                            if (x + dx, y + dy, z + dz, w + dw) in active_cubes:
                                                active_neighbors += 1
                        # Apply Conway's rules
                        if (x, y, z, w) in active_cubes and active_neighbors in [2, 3]:
                            next_active_cubes.add((x, y, z, w))
                        elif (x, y, z, w) not in active_cubes and active_neighbors == 3:
                            next_active_cubes.add((x, y, z, w))

        active_cubes = next_active_cubes

    return len(active_cubes)

# Initialize active cubes for Part 2 (4D)
def parse_input_to_active_4d(input_data):
    active_cubes = set()
    for row, line in enumerate(input_data):
        for col, char in enumerate(line):
            if char == '#':
                active_cubes.add((row, col, 0, 0))
    return active_cubes

# Solve Part 2
active_cubes_4d = parse_input_to_active_4d(input_data)
print(f'Part 2: {evolve_grid_4d(active_cubes_4d)}')
