# Advent of Code - Day 20, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/20
# Solution by: [abbasmoosajee07]
# Brief: [Particle Racing]

import os, re, copy
import pandas as pd
import numpy as np
from collections import defaultdict

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

with open(D20_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_particle_data(particle_list):
    # Initialize a dictionary to store the structured data
    data = {
        'p_x': [], 'p_y': [], 'p_z': [],
        'v_x': [], 'v_y': [], 'v_z': [],
        'a_x': [], 'a_y': [], 'a_z': [],
        'pos': []
    }

    # Regular expression to extract numbers from the particle string
    pattern = r"p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>"

    # Process each particle entry in the list
    for particle in particle_list:
        # Extract values
        match = re.match(pattern, particle)
        if match:
            p_x, p_y, p_z, v_x, v_y, v_z, a_x, a_y, a_z = map(int, match.groups())

            # Append to respective lists in the dictionary
            data['p_x'].append(p_x)
            data['p_y'].append(p_y)
            data['p_z'].append(p_z)
            data['v_x'].append(v_x)
            data['v_y'].append(v_y)
            data['v_z'].append(v_z)
            data['a_x'].append(a_x)
            data['a_y'].append(a_y)
            data['a_z'].append(a_z)
            data['pos'].append((p_x) + (p_y) + (p_z))
    # Convert dictionary to DataFrame
    df = pd.DataFrame(data)
    return df


# Function to change particle properties
def change_particle_props(particle_props):
    particle_props["v_x"] += particle_props["a_x"]
    particle_props["v_y"] += particle_props["a_y"]
    particle_props["v_z"] += particle_props["a_z"]
    
    particle_props["p_x"] += particle_props["v_x"]
    particle_props["p_y"] += particle_props["v_y"]
    particle_props["p_z"] += particle_props["v_z"]
    
    # Calculate Manhattan distance from origin
    particle_props["pos"] = abs(particle_props["p_x"]) + abs(particle_props["p_y"]) + abs(particle_props["p_z"])
    
    return particle_props

# Function to update particle positions in the DataFrame
def change_particle_pos(properties_df):
    for n in range(len(properties_df)):
        properties_df.loc[n] = change_particle_props(properties_df.loc[n])
    return properties_df

# Collision detection and removal function
def remove_collisions(properties_df):
    # Create a dictionary to track positions and associated indices
    pos_dict = defaultdict(list)
    for index, row in properties_df.iterrows():
        pos = (row["p_x"], row["p_y"], row["p_z"])
        pos_dict[pos].append(index)
    
    # Identify collisions and remove them
    collision_indices = [indices for indices in pos_dict.values() if len(indices) > 1]
    for indices in collision_indices:
        properties_df.drop(indices, inplace=True)
    
    # Reset index to keep DataFrame indices consistent
    properties_df.reset_index(drop=True, inplace=True)
    return properties_df

def find_closest_particle(properties_df):
    # Calculate acceleration magnitude for each particle
    properties_df["acceleration_magnitude"] = (
        properties_df["a_x"].abs() + properties_df["a_y"].abs() + properties_df["a_z"].abs()
    )
    
    # Identify the particle with the smallest acceleration magnitude
    min_accel_particles = properties_df[properties_df["acceleration_magnitude"] == properties_df["acceleration_magnitude"].min()]
    
    # If there's only one particle with the smallest acceleration magnitude, return it
    if len(min_accel_particles) == 1:
        closest_particle = min_accel_particles.index[0]
    else:
        # If there are ties in acceleration, choose the one with the smallest velocity magnitude
        min_accel_particles["velocity_magnitude"] = (
            min_accel_particles["v_x"].abs() + min_accel_particles["v_y"].abs() + min_accel_particles["v_z"].abs()
        )
        closest_particle = min_accel_particles[min_accel_particles["velocity_magnitude"] == min_accel_particles["velocity_magnitude"].min()].index[0]
    
    return closest_particle


properties_df = parse_particle_data(input_data)

# Find the particle closest to the origin in the long term
closest_particle = find_closest_particle(properties_df)
print("The particle that will stay closest to the origin is:", closest_particle)


min_pos_list = []
# Initialize particles from input data
properties_df = parse_particle_data(input_data)

# Simulation loop for a set number of time steps
for time in range(0, 50):  # Run for 40 steps
    properties_df = change_particle_pos(properties_df)
    properties_df = remove_collisions(properties_df)  # Remove colliding particles
    min_pos = min(properties_df["pos"])

    # Output the minimum position and particle count each time step
    # print(f"Time: {time}, Closest Distance to Origin: {min_pos}, Particles Remaining: {len(properties_df)}")

    # Check if the last 'last_n' minimum positions are the same
    min_pos_list.append(min_pos)  # Append current minimum position to the list

print(f"Time: {time}, Closest Distance to Origin: {min_pos}, Particles Remaining: {len(properties_df)}")
