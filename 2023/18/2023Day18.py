"""Advent of Code - Day 18, Year 2023
Solution Started: Jan 8, 2025
Puzzle Link: https://adventofcode.com/2023/day/18
Solution by: abbasmoosajee07
Brief: [Dig holes and Lava Flow]
"""

#!/usr/bin/env python3

import os, re, copy, time
from math import gcd
import numpy as np
import pandas as pd
start_time = time.time()

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_list: list[str]) -> list[dict]:
    direction_mapping = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}
    instructions = []

    for line in input_list:
        # Split the input into direction, magnitude, and color
        dir, mag, color = line.split(' ')

        # Extract the numeric magnitude and hex-based values from the color
        color_value = color.strip('(#)')
        hex_mag = int(color_value[:-1], 16)
        direction_index = int(color_value[-1])  # Extract the last digit for direction

        # Map the direction index to a direction
        new_dir = direction_mapping[direction_index]

        # Store both small and large hole properties
        instructions.append({
            'small': (dir, int(mag)),
            'large': (new_dir, hex_mag),
        })
    return instructions

def dig_hole(instructions: tuple, hole_size: str) -> dict:
    """Returns a dict representing the corners of a hole with movements and color."""
    DIRECTIONS = {'U': ((-1, 0), '^'), 'D': ((1, 0), 'v'), 'R': ((0, 1), '>'), 'L': ((0, -1), '<')}
    basic_hole = {}
    row, col = (0, 0)

    # Process each instruction and record direction and color
    for hole_props in instructions:
        dir_ins, magnitude = hole_props[hole_size]
        (dr, dc), str_dir = DIRECTIONS[dir_ins]
        row += dr * magnitude
        col += dc * magnitude
        basic_hole[(row, col)] = (str_dir)
    return basic_hole, surveyors_formula(basic_hole)

def surveyors_formula(coords_dict: dict) -> int:
    """
    Efficiently calculates the area and perimeter of a polygon using the Shoelace Theorem
    and boundary lattice point calculation with GCD.
    """
    # Extract the coordinates
    coords = list(coords_dict.keys())
    n = len(coords)

    # Initialize the area and boundary point counter
    area = 0
    boundary_points = 0

    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]  # Wrap around to the first point

        # Shoelace formula for area
        area += (x1 * y2) - (x2 * y1)

        # Boundary points on the current edge
        boundary_points += gcd(abs(x2 - x1), abs(y2 - y1))

    # Calculate the absolute area and apply Pick's Theorem
    area = abs(area) // 2
    total_lattice_points = area + boundary_points // 2 + 1

    return total_lattice_points

dig_instructions = parse_input(input_data)

hole_p1, area_p1= dig_hole(dig_instructions, 'small')
print(f"Part 1: {area_p1}")

hole_p2, area_p2 = dig_hole(dig_instructions, 'large')
print(f"Part 2: {area_p2}")

# print(f"Execution Time = {time.time() - start_time:.5f}s")