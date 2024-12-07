"""Advent of Code - Day 6, Year 2024
Solution Started: Dec 6, 2024
Puzzle Link: https://adventofcode.com/2024/day/6
Solution by: abbasmoosajee07
Brief: [Guard Movements]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()
# Load the input data from the specified file path
D06_file = "Day06_input.txt"
D06_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D06_file)

# Read and sort input data into a grid
with open(D06_file_path) as file:
    input_data = file.read().strip().split('\n')
    grid = [list(row) for row in input_data]

# Parse obstacles and start position
def find_positions(input_grid):
    obstacles = set()
    init_r, init_c = 0, 0
    for row, line in enumerate(grid):
            for col, point in enumerate(line):
                if point == "#":
                    obstacles.add((col, row))
                elif point == "^":
                    init_r, init_c = col, row
    return (init_r, init_c), obstacles

# Function to traverse the path
def traverse_path(start, obstacles, bound):
    init_r, init_c = start
    visited = set()
    visited.add((init_r, init_c))

    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Left, Down, Right, Up
    dir_idx = 0

    cache = set()
    cache.add((init_r, init_c, dir_idx))

    while True:
        # Calculate the new position
        dir_r, dir_c = directions[dir_idx]
        new_r, new_c = init_r + dir_r, init_c + dir_c

        # If we hit an obstacle -> turn
        if (new_r, new_c) in obstacles:
            dir_idx = (dir_idx + 1) % 4

        # If we hit the boundary -> exit
        elif not (0 <= new_r < bound and 0 <= new_c < bound):
            return False, visited

        # Else -> move forward
        else:
            init_r, init_c = new_r, new_c
            visited.add((init_r, init_c))

            # Check for loop
            cache_key = (init_r, init_c, dir_idx)
            if cache_key in cache:
                return True, visited
            else:
                cache.add(cache_key)

start, obstacles = find_positions(grid)
# Part 1: Calculate visited positions
bound = len(grid)

_, visited = traverse_path(start, obstacles, bound)
print("Part 1:", len(visited))

# Part 2: Find candidates for new obstacles
candidates = visited - {start}
loop_count = 0

for cand in candidates:
    if traverse_path(start, obstacles | {cand}, bound)[0]:
        loop_count += 1

print("Part 2:", loop_count)
print(f"Execution Time: {time.time() - start_time:.4f} seconds")
