"""Advent of Code - Day 14, Year 2024
Solution Started: Dec 14, 2024
Puzzle Link: https://adventofcode.com/2024/day/14
Solution by: abbasmoosajee07
Brief: [Find Easter Egg]
"""

# #!/usr/bin/env python3

import os, re, copy,time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

# Load input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

# Read and sort input data into a grid
with open(D14_file_path) as file:
    input_data = file.read().strip().split('\n')
GRID_SIZE = (101, 103)
X, Y = GRID_SIZE
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Directions for BFS


def parse_input(particle_list):
    """Parse the input data into a dictionary of particles."""
    particle_dict = {}
    for particle_no, particle_properties in enumerate(particle_list):
        p_x, p_y, v_x, v_y = map(int, re.findall(r'-?\d+', particle_properties))
        particle_dict[particle_no] = {'p_x': p_x, 'p_y': p_y, 'v_x': v_x, 'v_y': v_y}
    return particle_dict

def update_particle_position(properties, grid_size = GRID_SIZE):
    """Update a particle's position based on its velocity."""
    properties['p_x'] += properties['v_x']
    properties['p_y'] += properties['v_y']
    properties['p_x'] %= grid_size[0]
    properties['p_y'] %= grid_size[1]

def calculate_safety_score(particles, grid_size = GRID_SIZE):
    """Calculate the safety score based on particle positions in quadrants."""
    quadrant_counts = [0, 0, 0, 0]  # Quadrant counts: [Q1, Q2, Q3, Q4]
    
    for properties in particles.values():
        final_x, final_y = properties['p_x'], properties['p_y']

        # Exclude midpoint
        if final_x == grid_size[0] // 2 or final_y == grid_size[1] // 2:
            continue

        # Correct quadrant assignment
        if 0 <= final_x < grid_size[0] // 2 and 0 <= final_y < grid_size[1] // 2:
            quadrant_counts[0] += 1  # Quadrant 1
        elif grid_size[0] // 2 < final_x < grid_size[0] and 0 <= final_y < grid_size[1] // 2:
            quadrant_counts[1] += 1  # Quadrant 2
        elif 0 <= final_x < grid_size[0] // 2 and grid_size[1] // 2 < final_y < grid_size[1]:
            quadrant_counts[2] += 1  # Quadrant 3
        elif grid_size[0] // 2 < final_x < grid_size[0] and grid_size[1] // 2 < final_y < grid_size[1]:
            quadrant_counts[3] += 1  # Quadrant 4

    # Safety score is the product of particles in each quadrant
    return quadrant_counts[0] * quadrant_counts[1] * quadrant_counts[2] * quadrant_counts[3]

def find_connected_components(grid):
    """Find the number of connected components of particles in the grid."""
    components = 0
    SEEN = set()

    # BFS to find connected components
    for x in range(X):
        for y in range(Y):
            if grid[y][x] == '#' and (x, y) not in SEEN:
                components += 1
                Q = deque([(x, y)])
                while Q:
                    x2, y2 = Q.popleft()
                    if (x2, y2) in SEEN:
                        continue
                    SEEN.add((x2, y2))
                    for dx, dy in DIRS:
                        xx, yy = x2 + dx, y2 + dy
                        if 0 <= xx < X and 0 <= yy < Y and grid[yy][xx] == '#':
                            Q.append((xx, yy))
    return components

def visualize_particles(grid, time_step, file_path='grid_output.txt'):
    """Visualize the grid and append it to a text file."""
    # Prepare the header for this time step
    time_step_header = f"\n--- Time Step {time_step} ---\n"

    # Convert the grid into a string representation
    text_grid = '\n'.join(''.join(row) for row in grid)


    # Append the grid for this time step to the file
    with open(file_path, 'a') as file:
        file.write(time_step_header)
        file.write(text_grid)
        file.write("\n")  # Add an empty line after each time step grid for separation

    print(f"Grid for time step {time_step} saved to {file_path}")

particles = parse_input(input_data)

for min in range(1, GRID_SIZE[0]*GRID_SIZE[1] * len(particles)):  # Start from 101 as Part 1 already simulated the first 100 steps
    # Update positions for the next time step
    for properties in particles.values():
        update_particle_position(properties, GRID_SIZE)

    # Calculate safety score
    safety_score = calculate_safety_score(particles, GRID_SIZE)

    if min == 100: # Part 1 time
        print(f"Part 1: {safety_score}")

    # Check for fewer than 200 connected components
    grid = [[' ' for _ in range(X)] for _ in range(Y)]
    for properties in particles.values():
        x, y = properties['p_x'], properties['p_y']
        grid[y][x] = '#'

    components = find_connected_components(grid)

    # Track the minimum safety score and time step with fewer than 200 components
    if components <= 200:
        easter_egg = True
        visualize_particles(grid, min, file_path= 'christmas_tree.txt')
        print(f"Part 2: {min}")
        break
    else:
        easter_egg = None
if easter_egg is None:
    print("Part 2: No Christmas Tree Found")
