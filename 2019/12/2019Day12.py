# Advent of Code - Day 12, Year 2019
# Solution Started: Nov 19, 2024
# Puzzle Link: https://adventofcode.com/2019/day/12
# Solution by: [abbasmoosajee07]
# Brief: [Modelling Jupyter's Moons]

#!/usr/bin/env python3

import os, re, copy, math
import numpy as np
import pandas as pd
from functools import reduce

# Load the input data from the specified file path
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read and sort input data into a grid
with open(D12_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_particle_data(particle_list):
    # Initialize a dictionary to store the structured data
    data = {
        'p_x': [], 'p_y': [], 'p_z': [],
        'v_x': 0, 'v_y': 0, 'v_z': 0
        # 'pos': []
        }

    # Regular expression to extract numbers from the particle string
    pattern = r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>"

    # Process each particle entry in the list
    for particle in particle_list:
        # Extract values
        match = re.match(pattern, particle)
        if match:
            p_x, p_y, p_z = map(int, match.groups())

            # Append to respective lists in the dictionary
            data['p_x'].append(p_x)
            data['p_y'].append(p_y)
            data['p_z'].append(p_z)
            # data['pos'].append((p_x) + (p_y) + (p_z))
    # Convert dictionary to DataFrame
    df = pd.DataFrame(data)
    return df

def compare_particles(particle, other_df, dim):
    # Get the value of the current particle in the specified dimension
    og_v = particle[dim]
    
    # Compare all other particles in the same dimension
    n_v = sum(other_df[dim] > og_v) - sum(other_df[dim] < og_v)
    
    return n_v

def calculate_gravity(all_particle):
    # Create a copy to avoid modifying the original DataFrame during iteration
    updated_particle = all_particle.copy()

    # Iterate over each particle
    for particle_no in range(len(all_particle)):
        # Get the current particle properties (row)
        particle_props = all_particle.iloc[particle_no]

        # Filter out the current particle
        other_particles = all_particle.drop(index=all_particle.index[particle_no])

        # Update velocity and position for each dimension
        for dim in ['p_x', 'p_y', 'p_z']:
            # Corresponding velocity key: v_x, v_y, v_z
            velocity_key = 'v_' + dim[-1]              # Calculate the velocity change
            nv = compare_particles(particle_props, other_particles, dim)
            # Update velocity
            updated_particle.at[particle_no, velocity_key] += nv
            # Update position
            updated_particle.at[particle_no, dim] += updated_particle.at[particle_no, velocity_key]
    return updated_particle

def calc_total_energy(particle_df):

    total_energy = 0
    for particle_no in range(len(particle_df)):
        particle_prop = particle_df.loc[particle_no]
        potential_E = abs(particle_prop['p_x']) + abs(particle_prop['p_y']) + abs(particle_prop['p_z'])
        kinetic_E = abs(particle_prop['v_x']) + abs(particle_prop['v_y']) + abs(particle_prop['v_z'])
        total_energy += potential_E * kinetic_E

    return total_energy

# Function to calculate LCM of two numbers
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

# Function to calculate LCM of a list of numbers
def lcm_multiple(numbers):
    return reduce(lcm, numbers)

def find_cycle_length(initial_positions, initial_velocities):
    num_particles = len(initial_positions)
    positions = initial_positions[:]
    velocities = initial_velocities[:]
    step = 0

    while True:
        # Update velocities
        for i in range(num_particles):
            for j in range(num_particles):
                if positions[i] < positions[j]:
                    velocities[i] += 1
                elif positions[i] > positions[j]:
                    velocities[i] -= 1

        # Update positions
        for i in range(num_particles):
            positions[i] += velocities[i]

        step += 1

        # Check if positions and velocities have returned to initial state
        if positions == initial_positions and velocities == initial_velocities:
            return step

# Main logic for Part 2
def steps_to_first_cycle(parsed_data):

    # Extract initial positions for each dimension
    initial_x = list(parsed_data['p_x'])
    initial_y = list(parsed_data['p_y'])
    initial_z = list(parsed_data['p_z'])

    # Initial velocities are all zero
    initial_velocities = [0] * len(initial_x)

    # Find cycle length for each dimension
    cycle_x = find_cycle_length(initial_x, initial_velocities)
    cycle_y = find_cycle_length(initial_y, initial_velocities)
    cycle_z = find_cycle_length(initial_z, initial_velocities)

    # Calculate the LCM of the cycle lengths
    return lcm_multiple([cycle_x, cycle_y, cycle_z])


initial_df = parse_particle_data(input_data)
particle_df = initial_df

for steps in range(1000):
    particle_df = calculate_gravity(particle_df)

ans_p1 = calc_total_energy(particle_df)
print(f"Part 1: {ans_p1}")

# Solve Part 2
ans_p2 = steps_to_first_cycle(initial_df)
print(f"Part 2: {ans_p2}")
