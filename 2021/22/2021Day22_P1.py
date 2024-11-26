# Advent of Code - Day 22, Year 2021
# Solution Started: Nov 26, 2024
# Puzzle Link: https://adventofcode.com/2021/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Cubes, a lot of Cubes P1]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Read and sort input data into a grid
with open(D22_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_instruction(instruction_list):
    complete_dict = []
    for instruction in instruction_list:
        # Use regex to match the pattern
        pattern = r"(?P<action>\w+) x=(?P<x_start>-?\d+)..(?P<x_end>-?\d+),y=(?P<y_start>-?\d+)..(?P<y_end>-?\d+),z=(?P<z_start>-?\d+)..(?P<z_end>-?\d+)"
        match = re.match(pattern, instruction)

        if match:
            instruction_dict = {
                "action": match.group("action"),
                "x_range": (int(match.group("x_start")), int(match.group("x_end"))),
                "y_range": (int(match.group("y_start")), int(match.group("y_end"))),
                "z_range": (int(match.group("z_start")), int(match.group("z_end"))),
            }
        complete_dict.append(instruction_dict)
    return complete_dict

# Example usage
instruction_dict = parse_instruction(input_data)

def create_cuboid(cuboid_info, limit = 50):
    cube_coords = set()
    x1, x2 = cuboid_info['x_range']
    y1, y2 = cuboid_info['y_range']
    z1, z2 = cuboid_info['z_range']

    # Ensure the ranges are correct: always iterate from the smaller value to the larger value
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    z_min, z_max = min(z1, z2), max(z1, z2)

    # Check if all coordinates are within the valid range of -limit to limit
    if -limit <= x_min <= limit and -limit <= x_max <= limit and -limit <= y_min <= limit \
        and -limit <= y_max <= limit and -limit <= z_min <= limit and -limit <= z_max <= limit:
        # Iterate through all points within the cuboid range
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    cube_coords.add((x, y, z))
    else:
        cube_coords = set()
    return cube_coords

full_grid = set()

# Assuming instruction_dict is a list of dictionaries with 'action' and range information
for instruction in instruction_dict:
    cube_coords = create_cuboid(instruction)
    if instruction['action'] == 'on':
        full_grid.update(cube_coords)
    elif instruction['action'] == 'off':
        full_grid.difference_update(cube_coords)

# Print the result (total number of cubes turned on)
print("Part 1:", len(full_grid))
