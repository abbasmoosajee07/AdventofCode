# Advent of Code - Day 24, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/24
# Solution by: [abbasmoosajee07]
# Brief: [HEX Grid Navigation]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read and sort input data into a grid
with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_data = [re.findall(r"e|se|sw|w|nw|ne", row) for row in input_data]

# Hex grid directions (row, col adjustments)
DIRECTIONS = {
    "e": (0, 1),
    "w": (0, -1),
    "se": (1, 1),
    "sw": (1, 0),
    "nw": (-1, -1),
    "ne": (-1, 0),
}


def move_to_position(directions):
    """Given a list of directions, compute the final position on the hex grid."""
    row, col = 0, 0
    for dir in directions:
        dr, dc = DIRECTIONS[dir]
        row += dr
        col += dc
    return row, col

def flip_tiles(input_data):
    """Simulate flipping tiles based on directions."""
    black_tiles = set()

    for directions in input_data:
        pos = move_to_position(directions)
        if pos in black_tiles:
            black_tiles.remove(pos)  # Flip back to white
        else:
            black_tiles.add(pos)  # Flip to black

    return black_tiles

def count_black_neighbors(pos, black_tiles):
    """Count the number of black neighbors for a given tile."""
    row, col = pos
    return sum(
        (row + dr, col + dc) in black_tiles
        for dr, dc in DIRECTIONS.values()
    )

def simulate_days(black_tiles, days=100):
    """Simulate flipping tiles over multiple days."""
    for _ in range(days):
        # Expand grid to include all possible neighbors
        candidates = set(
            (row + dr, col + dc)
            for row, col in black_tiles
            for dr, dc in DIRECTIONS.values()
        ) | black_tiles

        # Determine new state of tiles
        new_black_tiles = set()
        for pos in candidates:
            black_neighbors = count_black_neighbors(pos, black_tiles)
            if pos in black_tiles and black_neighbors in (1, 2):
                new_black_tiles.add(pos)
            elif pos not in black_tiles and black_neighbors == 2:
                new_black_tiles.add(pos)

        black_tiles = new_black_tiles

    return black_tiles


# Part 1: Flip tiles based on input
black_tiles = flip_tiles(input_data)
print("Part 1:", len(black_tiles))

# Part 2: Simulate 100 days
black_tiles_after_100_days = simulate_days(black_tiles, days=100)
print("Part 2:", len(black_tiles_after_100_days))
