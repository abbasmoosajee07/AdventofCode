# Advent of Code - Day 11, Year 2021
# Solution Started: Nov 24, 2024
# Puzzle Link: https://adventofcode.com/2021/day/11
# Solution by: [abbasmoosajee07]
# Brief: [Energy Flashes and grids]

#!/usr/bin/env python3

import os, re, copy,heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path) as file:
    input_data = file.read().strip().split('\n')
    num_list = [[int(num) for num in list(row)]
                    for row in input_data ]
    energy_map = np.array(num_list)

# Directions for the 8 possible neighbors of an octopus (up, down, left, right, and diagonals)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Function to simulate one step of the flashing process
def simulate_step(energy_map):
    total_rows, total_cols = energy_map.shape
    flashed = np.zeros_like(energy_map, dtype=bool)  # Keep track of which octopuses have flashed
    
    # Increase the energy of all octopuses by 1
    energy_map += 1

    # Flashing process
    flashes = 0
    while True:
        # Find all octopuses that have energy >= 10 and have not flashed yet
        flash_positions = np.argwhere((energy_map >= 10) & ~flashed)
        
        if flash_positions.size == 0:
            break  # No more flashes, stop the loop

        # For each octopus that flashes
        for r, c in flash_positions:
            # Reset energy of the octopus that flashed
            energy_map[r, c] = 0
            flashed[r, c] = True
            flashes += 1

            # Increase the energy of the neighboring octopuses
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < total_rows and 0 <= nc < total_cols:
                    if not flashed[nr, nc]:  # Only increase energy of octopuses that have not flashed yet
                        energy_map[nr, nc] += 1

    return flashes

# Part 1: Calculate the total number of flashes after 100 steps
def solve_part_1(energy_map, steps=100):
    total_flashes = 0
    for _ in range(steps):
        flashes = simulate_step(energy_map)
        total_flashes += flashes
    return total_flashes

# Part 2: Find the first step where all octopuses flash at once
def solve_part_2(energy_map):
    total_steps = 0
    total_octopuses = energy_map.size
    while True:
        total_steps += 1
        flashes = simulate_step(energy_map)
        if flashes == total_octopuses:
            return total_steps

# Run Part 1
energy_map_copy_part1 = np.copy(energy_map)
total_flashes_part1 = solve_part_1(energy_map_copy_part1)
print(f"Part 1: Total number of flashes after 100 steps = {total_flashes_part1}")

# Run Part 2
energy_map_copy_part2 = np.copy(energy_map)
first_sync_step = solve_part_2(energy_map_copy_part2)
print(f"Part 2: The first step when all octopuses flash = {first_sync_step}")
