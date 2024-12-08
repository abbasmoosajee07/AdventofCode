"""Advent of Code - Day 18, Year 2022
Solution Started: Dec 7, 2024
Puzzle Link: https://adventofcode.com/2022/day/18
Solution by: abbasmoosajee07
Brief: [3D Cubes]
"""

#!/usr/bin/env python3

import os, re, copy, itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict, deque

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')
    cube_dimensions = set(tuple(map(int, row.split(','))) for row in input_data)


def get_cube_sides(x, y, z):
    """
    Generate all 6 sides of a cube at position (x, y, z).
    """
    sides = [
        (x+1, y, z),  # Right
        (x-1, y, z),  # Left
        (x, y+1, z),  # Top
        (x, y-1, z),  # Bottom
        (x, y, z+1),  # Front
        (x, y, z-1)   # Back
    ]
    return sides

# Determine if a position reaches outside using flood-fill
def reaches_outside(x, y, z, cube_list, out_set, in_set, threshold = 0):
    """
    Check if the position (x, y, z) reaches the outside of the structure.
    Uses flood-fill to explore.
    """
    if (x, y, z) in out_set:
        return True
    if (x, y, z) in in_set:
        return False

    seen = set()
    queue = deque([(x, y, z)])

    while queue:
        cx, cy, cz = queue.popleft()

        if (cx, cy, cz) in cube_list or (cx, cy, cz) in seen:
            continue

        seen.add((cx, cy, cz))

        # If the search grows beyond a threshold, assume it reaches outside
        if len(seen) > (threshold):
            out_set.update(seen)
            return True

        # Add all adjacent positions to the queue
        queue.extend(get_cube_sides(cx, cy, cz))

    in_set.update(seen)
    return False

# Solve for the total or exposed surface area
def calculate_surface_area(cube_list, threshold):
    """
    Calculate the total surface area or exposed surface area.
    """
    out_set = set()
    in_set = set()
    exposed_area = 0

    for x, y, z in cube_list:
        for xn, yn, zn in get_cube_sides(x, y, z):
            if reaches_outside(xn, yn, zn, cube_list, out_set, in_set, threshold):
                exposed_area += 1

    return exposed_area

# Solve for Part 1 and Part 2
ans_p1 = calculate_surface_area(cube_dimensions, 0)
ans_p2 = calculate_surface_area(cube_dimensions, 4500)

print(f"Part 1: {ans_p1}")
print(f"Part 2: {ans_p2}")
