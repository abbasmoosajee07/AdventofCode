# Advent of Code - Day 13, Year 2021
# Solution Started: Nov 24, 2024
# Puzzle Link: https://adventofcode.com/2021/day/13
# Solution by: [abbasmoosajee07]
# Brief: [Origami w/ Code]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

# Read and sort input data into a grid
with open(D13_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    # Parse the input into a list of coordinate tuples
    marker_coords = [
        tuple(map(int, coord.split(',')))  # Convert each "x,y" pair to (x, y)
        for coord in input_data[0].strip().split('\n')  # Split by lines and process each
    ]
        # Parse fold instructions
    folds = [
        (line.split("=")[0][-1], int(line.split("=")[1])) for line in input_data[1].splitlines()
    ]

def apply_fold(marker_coords, axis, value):
    new_coords = set()
    for x, y in marker_coords:
        if axis == 'x':  # Vertical fold
            new_coords.add((value - abs(x - value), y) if x > value else (x, y))
        elif axis == 'y':  # Horizontal fold
            new_coords.add((x, value - abs(y - value)) if y > value else (x, y))
    return new_coords

def solve_part_1(marker_coords, folds):
    axis, value = folds[0]
    folded_coords = apply_fold(marker_coords, axis, value)
    return len(folded_coords)

def solve_part_2(marker_coords, folds):
    for axis, value in folds:
        marker_coords = apply_fold(marker_coords, axis, value)
    return marker_coords

def visualize_grid(marker_coords):
    max_x = max(x for x, y in marker_coords)
    max_y = max(y for x, y in marker_coords)
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in marker_coords:
        grid[y][x] = "|"
    for row in grid:
        print("".join(row))


# Part 1
print("Part 1:", solve_part_1(marker_coords, folds))

# Part 2
final_coords = solve_part_2(marker_coords, folds)
print("Part 2:")
visualize_grid(final_coords)