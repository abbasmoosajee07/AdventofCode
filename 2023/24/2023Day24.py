"""Advent of Code - Day 24, Year 2023
Solution Started: Jan 15, 2025
Puzzle Link: https://adventofcode.com/2023/day/24
Solution by: abbasmoosajee07
Brief: [3D Particle Interactions]
"""

#!/usr/bin/env python3

import os, re, copy, time
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

def identify_2d_interactions(particle_1: tuple, particle_2: tuple, target_area: tuple) -> bool:
    min_size, max_size = target_area
    # Unpack particle 1 and particle 2 data
    ((px_1, py_1, _), (vx_1, vy_1, _)) = particle_1
    ((px_2, py_2, _), (vx_2, vy_2, _)) = particle_2

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
                interaction = identify_2d_interactions(properties_1, properties_2, target_area)
                if interaction:
                    particle_interactions.add((combo, interaction))
                count += 1
                # if count % 1000 == 0:
                #     print(f"Count {count} = {time.time() - start_time:.5f}")
    return particle_interactions

def find_perfect_throw(particle_data: dict) -> tuple:
    import sympy as sp

    particles = list(particle_data.keys())
    first_three_hailstones = []
    for particle_no in particles[:3]:
        (px_1, py_1, pz_1), (vx_1, vy_1, vz_1) = particle_data[particle_no]
        first_three_hailstones.append(tuple((px_1, py_1, pz_1, vx_1, vy_1, vz_1)))

    x, y, z, dx, dy, dz, *time = sp.symbols('x, y, z, dx, dy, dz, t1, t2, t3')

    equations = []  # build system of 9 equations with 9 unknowns
    for t, h in zip(time, first_three_hailstones):
        equations.append(sp.Eq(x + t*dx, h[0] + t*h[3]))
        equations.append(sp.Eq(y + t*dy, h[1] + t*h[4]))
        equations.append(sp.Eq(z + t*dz, h[2] + t*h[5]))

    solution = sp.solve(equations, (x, y, z, dx, dy, dz, *time)).pop()
    return solution

particle_data = parse_input(input_data)
total_interactions  = simulate_all_particles(particle_data, target_area=(2E+14, 4E+14))
print("Part 1:", len(total_interactions))

thrown_particle = find_perfect_throw(particle_data)
print("Part 2:", sum(thrown_particle[:3]))

# print(f"Execution Time = {time.time() - start_time:.5f}")

