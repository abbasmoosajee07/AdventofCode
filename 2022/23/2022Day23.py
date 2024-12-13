"""Advent of Code - Day 23, Year 2022
Solution Started: Dec 12, 2024
Puzzle Link: https://adventofcode.com/2022/day/23
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, re, copy 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict, deque

# Load the input data from the specified file path
D23_file = "Day23_input.txt"
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

# Read and sort input data into a grid
with open(D23_file_path) as file:
    input_data = file.read().strip().split('\n')

def starting_elf_position(init_map):
    init_array = [list(row) for row in init_map]
    elf_index = set()
    for row_no, row in enumerate(init_array):
        for col_no, char in enumerate(row):
            if char == '#':
                elf_index.add((row_no, col_no))
    return elf_index

def map_elves(elf_index):
    # Determine the grid size based on the maximum row and column values
    max_row = max(r for r, c in elf_index)
    max_col = max(c for r, c in elf_index)
    min_row = min(r for r, c in elf_index)
    min_col = min(c for r, c in elf_index)

    # Initialize an empty grid with '.' for unoccupied positions
    grid = [['.' for _ in range(min_col, max_col+1)] for _ in range(min_row, max_row +1)]

    # Mark the positions in the grid with '#'
    for r, c in elf_index:
        grid[r-min_row][c-min_col] = '#'

    # Display the grid
    # for row in grid:
    #     print(''.join(row))
    return grid

def move_elves(elf_index):
    # Define movement directions and offsets
    DIRECTION_OFFSETS = {
        'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)
    }
    DIAGONAL_OFFSETS = {
        'N': [(-1, -1), (-1, 1)], 'S': [(1, -1), (1, 1)],
        'W': [(-1, -1), (1, -1)], 'E': [(-1, 1), (1, 1)]
    }
    DIRECTIONS = ['N', 'S', 'W', 'E']

    for t in range(10000):
        any_moved = False
        # Dictionary to track desired positions and the elves that want to move there
        proposed_moves = defaultdict(list)

        # Determine proposed moves for each elf
        for (r, c) in elf_index:
            # Check if the elf has any neighbors
            has_neighbors = any(
                (r + dr, c + dc) in elf_index
                for dr in [-1, 0, 1] for dc in [-1, 0, 1] if (dr, dc) != (0, 0)
            )

            if not has_neighbors:
                continue  # Skip if no neighbors

            # Propose a move based on the current directions
            for dir_ in DIRECTIONS:
                move_offset = DIRECTION_OFFSETS[dir_]
                diagonal_offsets = DIAGONAL_OFFSETS[dir_]
                new_pos = (r + move_offset[0], c + move_offset[1])

                if (
                    new_pos not in elf_index and
                    all((r + dr, c + dc) not in elf_index for dr, dc in diagonal_offsets)
                ):
                    proposed_moves[new_pos].append((r, c))
                    break  # Stop after proposing one move

        # Rotate directions for the next round
        DIRECTIONS = DIRECTIONS[1:] + DIRECTIONS[:1]

        # Execute the moves
        for target, movers in proposed_moves.items():
            if len(movers) == 1:  # Move only if there's no conflict
                any_moved = True
                elf_index.discard(movers[0])
                elf_index.add(target)

        # Stop if no elves moved
        if not any_moved:
            ans_p2 = t + 1  # Part 2 answer is the round when movement stops
            break

        # Compute part 1 answer after 10 rounds
        if t == 9:
            grid_p1 = map_elves(elf_index)  # Assume map_elves converts the set into a grid
            ans_p1 = sum(row.count('.') for row in grid_p1)

    return ans_p1, ans_p2

elf_init = starting_elf_position(input_data)
ans_p1, ans_p2 = move_elves(elf_init)
print("Part 1:", ans_p1)
print("Part 2:", ans_p2)
