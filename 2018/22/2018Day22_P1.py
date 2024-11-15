# Advent of Code - Day 22, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Navigating Caves, P1]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Read and sort input data into a grid
with open(D22_file_path) as file:
    input_data = file.read().strip().split('\n')
    depth = int(input_data[0].strip('depth:'))
    target_str = input_data[1].strip('target:').split(',')
    target = list(map(lambda x: int(x.strip()), target_str))
print(input_data, depth, target)

def find_erosion_level(grid, depth, target, x, y):
    """
    The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    The region at the coordinates of the target has a geologic index of 0.
    If the region's Y coordinate is 0, 
        the geologic index is its X coordinate times 16807.
    If the region's X coordinate is 0, 
        the geologic index is its Y coordinate times 48271.
    Otherwise, the region's geologic index is the result of multiplying 
        the erosion levels of the regions at X-1,Y and X,Y-1.
    """
    erosion_level = 1
    if x == 0 and y == 0:
        geological_index = 0
    elif x == target[0] and y == target[1]:
        geological_index = 0
    elif x == 0:
        geological_index = 48271 * y
    elif y == 0:
        geological_index = 16807 * x
    else:
        geological_index = grid[y-1][x] * grid[y][x-1]

    erosion_level = (geological_index + depth) % 20183
    ground_type = erosion_level % 3
    return erosion_level, ground_type

def map_cave(depth, target):
    # Initialize count and grids separately
    count = 0
    erosion_grid = np.zeros((target[1] + 1, target[0] + 1))
    cave_grid = np.copy(erosion_grid)  # Create a separate grid with the same shape

    # Iterate through each element of the cave grid
    for y, row in enumerate(erosion_grid):
        for x, col in enumerate(row):
            erosion_level, ground = find_erosion_level(erosion_grid, depth, target, x, y)
            # print(x, y, erosion_level, ground)
            erosion_grid[y][x] = erosion_level
            cave_grid[y][x] = ground
            count += ground

    return cave_grid, count

cave_grid, ans_p1= map_cave(depth, target)
print(f"Part 1: {ans_p1}")

# for row in cave_grid:
#     print((row))
