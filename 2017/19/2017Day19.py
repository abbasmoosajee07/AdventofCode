# Advent of Code - Day 19, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/19
# Solution by: [abbasmoosajee07]
# Brief: [Directional Map]

import os, re, copy
import pandas as pd
import numpy as np
from collections import defaultdict

# Load the input data from the specified file path
D19_file = "Day19_input.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Open the file and read all lines into a list
lines = open(D19_file_path).read().splitlines()

# Create a dictionary to store the road map as a grid of points.
# Each key is a complex number representing a coordinate (x+1j*y),
# and the value is the character found at that position ('.', '-', '|', '+', or letters).
road = {
    x + 1j * y: v  # Position represented as complex number x + y*i
    for y, line in enumerate(lines)  # Enumerate over rows for y-axis positions
    for x, v in enumerate(line)      # Enumerate over each character in row for x-axis
    if v.strip()                     # Only include non-whitespace characters
}

# Set the initial direction to move "downward" in the complex plane (1j)
direction = 1j

# Find the starting position by locating the minimum y-coordinate in the road map (top of the grid)
# This is often the entry point, typically where the path begins in a given puzzle layout.
pos = min(road, key=lambda v: v.imag)

# Initialize an empty list to store the path we've taken as a sequence of positions
path = []

# Begin navigating through the road map until the position is no longer in the road
while pos in road:
    # Check if the current position has a '+' character, which indicates an intersection.
    # If so, adjust direction by checking possible turns (left or right).
    if road[pos] == '+':
        # Use next() to find a valid turn from the current direction.
        # Turns are checked in sequence for left (direction * 1j) and right (direction * -1j),
        # ensuring we avoid backtracking by checking that the move isn't from where we just came.
        direction = next(
            d for d in [direction * 1j, direction * -1j]  # Check left then right turns
            if pos + d in road and d != path[-1] - pos    # Avoid backtracking
        )

    # Record the current position in the path
    path += [pos]

    # Move to the next position based on the current direction
    pos += direction

# Join and print all alphabetic characters in the path to reveal the hidden word/message
P1_ans = ''.join(c for c in map(road.get, path) if c.isalpha())
print(f"Part 1: Pitstops on path are {P1_ans}")

# Print the total length of the path, which counts the number of steps taken
P2_ans = len(path)
print(f"Part 2: Steps taken on path are {P2_ans}")
