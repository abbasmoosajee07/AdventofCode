"""Advent of Code - Day 24, Year 2023
Solution Started: Jan 15, 2025
Puzzle Link: https://adventofcode.com/2023/day/24
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, re, copy, time
import sympy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()
# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read and sort input data into a grid
with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_list: list[str]) -> dict[tuple]:
    particle_data = {}

    for particle_no, line in enumerate(input_list, start=1):
        position, velocity = line.split('@')
        position_no = tuple(map(int, position.split(', ')))
        velocity_no = tuple(map(int, velocity.split(', ')))
        particle_data[particle_no] = (position_no, velocity_no)
    return particle_data

def identify_interactions(particle_1: tuple, particle_2: tuple, target_area: tuple) -> int:
    min_size, max_size = target_area
    # Unpack particle 1 and particle 2 data
    ((px_1, py_1, pz_1), (vx_1, vy_1, vz_1)) = particle_1
    ((px_2, py_2, pz_2), (vx_2, vy_2, vz_2)) = particle_2

    # Compute slopes (m1 and m2)
    if vx_1 != 0 and vx_2 != 0:  # Ensure no division by zero
        m1 = vy_1 / vx_1
        m2 = vy_2 / vx_2

        # Check for non-parallel lines
        if m1 != m2:
            # Compute y-intercepts (b1 and b2)
            b1 = py_1 - m1 * px_1
            b2 = py_2 - m2 * px_2

            # Calculate intersection point (x, y)
            x = (b2 - b1) / (m1 - m2)
            y = m1 * x + b1

            # Check if intersection is within the target area and happens in the future
            if min_size <= x <= max_size and min_size <= y <= max_size:
                # Ensure the intersection happens in the future based on the direction of velocities
                if  ((x > px_1 and vx_1 > 0) or (x < px_1 and vx_1 < 0)) and \
                    ((x > px_2 and vx_2 > 0) or (x < px_2 and vx_2 < 0)):
                    return (x, y)

    return None  # Return None if no valid intersection is found

def simulate_all_particles(particle_data: dict, target_area: tuple):
    particle_interactions = set()
    combos_checked = set()
    count = 0

    for no_1, properties_1 in particle_data.items():
        for no_2, properties_2 in particle_data.items():
            combo = tuple(sorted((no_1, no_2)))
            if (no_1 != no_2) and (combo not in combos_checked):
                combos_checked.add(combo)
                interaction = identify_interactions(properties_1, properties_2, target_area)
                if interaction:
                    particle_interactions.add((combo, interaction))
                count += 1
                # if count % 1000 == 0:
                #     print(f"Count {count} = {time.time() - start_time:.5f}")
    return particle_interactions

test_input = ['19, 13, 30 @ -2,  1, -2', '18, 19, 22 @ -1, -1, -2', '20, 25, 34 @ -2, -2, -4', '12, 31, 28 @ -1, -2, -1', '20, 19, 15 @  1, -5, -3']

target_area = (200_000_000_000_000, 400_000_000_000_000)

particle_data = parse_input(input_data)
total_interactions  = simulate_all_particles(particle_data, target_area)
print("Part 1:", len(total_interactions))

# print(f"Execution Time = {time.time() - start_time:.5f}")
