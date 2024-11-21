# Advent of Code - Day 11, Year 2020
# Solution Started: Nov 20, 2024
# Puzzle Link: https://adventofcode.com/2020/day/11
# Solution by: [abbasmoosajee07]
# Brief: [Simulate Seating Chart]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path) as file:
    input_data = file.read().strip().split('\n')
    seating_chart = np.array([list(row) for row in input_data])

def get_neighbors(grid, pos, diagonals=True):
    # Directions for up, down, left, right (4 directions)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # If diagonals are allowed, add them
    if diagonals:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    full_seats = 0
    rows, cols = len(grid), len(grid[0])
    for dr, dc in directions:
        row, col = pos
        new_row, new_col = row + dr, col + dc
        # Check if the new position is within bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            seat = grid[(new_row, new_col)]
            if seat == '#':
                full_seats += 1
            elif seat in {'L', '.'}:
                full_seats += 0
    return full_seats

def get_visible_seats(grid, pos, diagonals=True):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    
    if diagonals:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Add Diagonals
    
    full_seats = 0
    rows, cols = len(grid), len(grid[0])

    for dr, dc in directions:
        row, col = pos

        # Move in the direction (dr, dc) by steps of GCD
        while True:
            row += dr
            col += dc
            
            # Check if out of bounds
            if not (0 <= row < rows and 0 <= col < cols):
                break

            seat = grid[row][col]
            
            # If the seat is empty or a floor, we continue checking in this direction
            if seat == '.':
                continue
            
            # If we encounter a seat, we stop searching in this direction
            if seat == '#':
                full_seats += 1
                break
            elif seat == 'L':
                # If it's an empty seat, we stop looking in this direction
                break

    return full_seats

def update_grid(grid, condition = 'nearby', max_occupancy = 4):
    new_grid = copy.deepcopy(grid)
    for row_no, row in enumerate(grid):
        for col_no, seat in enumerate(row):
            seat_coord = (row_no, col_no)
            if condition == 'nearby':
                full_seats = get_neighbors(grid, seat_coord)
            elif condition == 'visible':
                full_seats = get_visible_seats(grid, seat_coord)
            if seat == 'L' and full_seats == 0:
                new_grid[seat_coord] = '#'
            if seat == '#' and full_seats >= max_occupancy:
                new_grid[seat_coord] = 'L'
    return new_grid

def count_hashes(grid):
    return np.char.count(grid.astype(str), '#').sum()

def seating_changes(initial_chart, condition, max_occupancy):
    current_chart = initial_chart
    current_occupancy = float('inf')
    previous_occupancy = count_hashes(initial_chart)
    while current_occupancy != previous_occupancy:
        current_chart = update_grid(current_chart, condition, max_occupancy)
        previous_occupancy = current_occupancy
        current_occupancy = count_hashes(current_chart)
    final_occupancy = current_occupancy

    return final_occupancy

ans_p1 = seating_changes(seating_chart, 'nearby', 4)
print("Part 1:", ans_p1)

ans_p2 = seating_changes(seating_chart, 'visible', 5)
print("Part 2:", ans_p2)