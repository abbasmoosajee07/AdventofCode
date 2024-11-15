# Advent of Code - Day 23, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/23
# Solution by: [abbasmoosajee07]
# Brief: [Tracking bots position, P1]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D23_file = "Day23_input.txt"
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

# Read and sort input data into a grid
with open(D23_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_particle_data(particle_list):
    # Initialize a dictionary to store the structured data
    data = {
        'p_x': [], 'p_y': [], 'p_z': [], 'r': []
    }

    # Regular expression to extract numbers from the particle string
    pattern = r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)"  # Now matching only non-negative 'r'

    # Process each particle entry in the list
    for particle in particle_list:
        match = re.match(pattern, particle)
        if match:
            p_x, p_y, p_z, r = map(int, match.groups())
            # Append to respective lists in the dictionary
            data['p_x'].append(p_x)
            data['p_y'].append(p_y)
            data['p_z'].append(p_z)
            data['r'].append(r)

    return pd.DataFrame(data)

# Parse the data into a DataFrame
input_pos_df = parse_particle_data(input_data)

def find_particles_in_range(input_df, n):
    # Find the particle with the target signal radius
    target_particle = input_df.loc[n]
    target_radius = target_particle['r']

    # Calculate the number of particles within the range of the targetimum radius particle
    in_range_count = 0
    for _, row in input_df.iterrows():
        # Manhattan distance to the target radius particle
        distance = abs(row['p_x'] - target_particle['p_x']) + \
                   abs(row['p_y'] - target_particle['p_y']) + \
                   abs(row['p_z'] - target_particle['p_z'])
        
        # Check if within target particle's radius
        if distance <= target_radius:
            in_range_count += 1

    return in_range_count

# Calculate Part 1 answer
ans_p1 = find_particles_in_range(input_pos_df, input_pos_df['r'].idxmax())
print(f"Part 1: {ans_p1}")
