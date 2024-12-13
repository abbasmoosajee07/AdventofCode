"""Advent of Code - Day 22, Year 2022
Solution Started: Dec 11, 2024
Puzzle Link: https://adventofcode.com/2022/day/22
Solution by: abbasmoosajee07
Brief: [Moving in a 3D Cube]
"""

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
    input_data = file.read().split('\n\n')
    movements = re.findall(r'\d+|[RL]', input_data[1])
#!/usr/bin/env python3

import os
import re
import numpy as np

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Read and sort input data into a grid and movements
with open(D22_file_path) as file:
    input_data = file.read().split('\n\n')
    grid_data = input_data[0].split('\n')
    movements = re.findall(r'\d+|[RL]', input_data[1])

def build_grid(grid_lines):
    """Build a grid from the input string, padding rows to have equal length."""
    max_len = max(len(line) for line in grid_lines)
    padded_lines = [line.ljust(max_len) for line in grid_lines]
    return np.array([list(line) for line in padded_lines], dtype=str)

def calculate_final_password(position):
    """Calculate the final password based on the position."""
    row, col, direction = position
    direction_value = {0: 3, 1: 0, 2: 1, 3: 2}
    return (1000 * (row + 1)) + (4 * (col + 1)) + direction_value[direction]

def region_to_global(r, c, region):
    """Convert local coordinates within a region to global grid coordinates."""
    rr, cc = REGION[region - 1]
    return (rr * CUBE_SIZE + r, cc * CUBE_SIZE + c)

def get_region(r, c):
    """Get the region and local coordinates for a global grid position."""
    for i, (rr, cc) in enumerate(REGION):
        if rr * CUBE_SIZE <= r < (rr + 1) * CUBE_SIZE and cc * CUBE_SIZE <= c < (cc + 1) * CUBE_SIZE:
            return i + 1, r - rr * CUBE_SIZE, c - cc * CUBE_SIZE
    raise ValueError(f"Position ({r}, {c}) does not match any region")

def new_coords(r, c, d, nd):
    """Compute new coordinates on the cube after transitioning across a face boundary."""
    if d == 0:  # Moving up
        assert r == 0
        x = c
    elif d == 1:  # Moving right
        assert c == CUBE_SIZE - 1
        x = r
    elif d == 2:  # Moving down
        assert r == CUBE_SIZE - 1
        x = CUBE_SIZE - 1 - c
    elif d == 3:  # Moving left
        assert c == 0
        x = CUBE_SIZE - 1 - r

    if nd == 0:
        return CUBE_SIZE - 1, x
    elif nd == 1:
        return x, 0
    elif nd == 2:
        return 0, CUBE_SIZE - 1 - x
    elif nd == 3:
        return CUBE_SIZE - 1 - x, CUBE_SIZE - 1

def get_dest(r, c, d):
    """Get the destination position and new direction after moving off the current cube face."""
    region, rr, rc = get_region(r, c)

    # Mapping of exits and entries between faces based on direction
    new_region, new_dir = {
        (4, 0): (3, 0), (4, 1): (2, 3), (4, 2): (6, 3), (4, 3): (5, 3),
        (1, 0): (6, 1), (1, 1): (2, 1), (1, 2): (3, 2), (1, 3): (5, 1),
        (3, 0): (1, 0), (3, 1): (2, 0), (3, 2): (4, 2), (3, 3): (5, 2),
        (6, 0): (5, 0), (6, 1): (4, 0), (6, 2): (2, 2), (6, 3): (1, 2),
        (2, 0): (6, 0), (2, 1): (4, 3), (2, 2): (3, 3), (2, 3): (1, 3),
        (5, 0): (3, 1), (5, 1): (4, 1), (5, 2): (6, 2), (5, 3): (1, 1)
    }[(region, d)]

    # Calculate new coordinates on the new face and map to global grid
    nr, nc = new_coords(rr, rc, d, new_dir)
    nr, nc = region_to_global(nr, nc, new_region)
    return nr, nc, new_dir

def move_on_3d_cube():
    """Simulate the movement of the robot and calculate the final password."""
    # Initial robot position (top-left corner) and direction (right)
    r, c, d = 0, 0, 1
    while grid[r][c] != '.':
        c += 1  # Find the first valid position in the top row

    i = 0
    while i < len(movements):
        # Parse movement instructions
        n = 0
        while i < len(movements) and movements[i].isdigit():
            n = n * 10 + int(movements[i])
            i += 1

        # Process movement
        for _ in range(n):
            assert grid[r][c] == '.', f"Unexpected position: ({r}, {c})"
            rr = (r + DIRECTIONS[d][0]) % len(grid)
            cc = (c + DIRECTIONS[d][1]) % len(grid[0])
            if grid[rr][cc] == ' ':
                # Transition to a new face if moving off the current face
                nr, nc, nd = get_dest(r, c, d)
                if grid[nr][nc] == '#':
                    break  # Stop if hitting a wall
                r, c, d = nr, nc, nd
            elif grid[rr][cc] == '#':
                break  # Stop if hitting a wall
            else:
                r, c = rr, cc

        if i == len(movements):
            break

        # Handle turns
        turn = movements[i]
        if turn == 'L':
            d = (d + 3) % 4  # Left turn (counterclockwise)
        elif turn == 'R':
            d = (d + 1) % 4  # Right turn (clockwise)
        i += 1

    return calculate_final_password((r,c,d))

# Initial grid and movement setup
grid = build_grid(grid_data)

# Constants
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
CUBE_SIZE = len(grid[0]) // 3  # Assuming the grid is folded into a 3x3 cube
REGION = [(0, 1), (0, 2), (1, 1), (2, 1), (2, 0), (3, 0)]  # Cube face regions

# Output the result for part 2
print("Part 2:", move_on_3d_cube())
