# Advent of Code - Day 10, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/10
# Solution by: [abbasmoosajee07]
# Brief: [Particles,Boxes and Letters]

import os, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read and sort input data into a grid
with open(D10_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_particle_data(particle_list):
    # Initialize a dictionary to store the structured data
    data = {
        'p_x': [], 'p_y': [],
        'v_x': [], 'v_y': [],
        'pos': []
    }

    # Regular expression to extract numbers from the particle string
    # position=< 9,  1> velocity=< 0,  2>
    pattern = r"position=<\s*(-?\d+),\s*(-?\d+)>\s+velocity=<\s*(-?\d+),\s*(-?\d+)>"
    # Process each particle entry in the list
    for particle in particle_list:
        # Extract values
        match = re.match(pattern, particle)

        if match:
            p_x, p_y, v_x, v_y = map(int, match.groups())

            # Append to respective lists in the dictionary
            data['p_x'].append(p_x)
            data['p_y'].append(p_y)

            data['v_x'].append(v_x)
            data['v_y'].append(v_y)

            data['pos'].append((p_x) + (p_y))
    # Convert dictionary to DataFrame
    df = pd.DataFrame(data)
    return df

def create_message_grid(particle_props, time, show=False):
    # Update particle positions based on velocity and time (create a copy for updates)
    particle_pos = particle_props.copy()
    particle_pos["p_x"] += particle_pos["v_x"] * time
    particle_pos["p_y"] += particle_pos["v_y"] * time

    # Create a scatter plot
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.scatter(particle_pos["p_x"], particle_pos["p_y"], color='black', marker='o', label='Particles', s=7) 
    ax.set_xlabel('X Coordinate', fontsize=7)
    ax.set_ylabel('Y Coordinate', fontsize=7)
    ax.set_title(f'Particle Scatter Plot for Time = {time}') 
    ax.invert_yaxis()  # Optional: invert y-axis
    ax.grid(True)

    # Show the plot if specified
    # if show:
    #     display(fig)

    return particle_pos, fig

def calculate_bounding_box_area(particle_props):
    # Find the min and max values of the x and y positions
    min_x = particle_props["p_x"].min()
    max_x = particle_props["p_x"].max()
    min_y = particle_props["p_y"].min()
    max_y = particle_props["p_y"].max()

    # Calculate the area of the bounding box
    width = max_x - min_x
    height = max_y - min_y
    area = width * height

    return area, min_x, max_x, min_y, max_y

def find_minimum_area_time_range(particle_props, start_time, end_time):
    min_area = float('inf')
    best_time = start_time
    best_bounding_box = (None, None, None, None)

    # Track the area for each time step
    for time in range(start_time, end_time + 1):
        # Update particle positions
        current_pos = particle_props.copy()
        current_pos["p_x"] += current_pos["v_x"] * time
        current_pos["p_y"] += current_pos["v_y"] * time
        
        # Calculate the bounding box area
        area, min_x, max_x, min_y, max_y = calculate_bounding_box_area(current_pos)

        # Check if this area is the smallest so far
        if area < min_area:
            min_area = area
            best_time = time
            best_bounding_box = (min_x, max_x, min_y, max_y)

    return best_time, min_area, best_bounding_box


particle_df = parse_particle_data(input_data)

# Use this function to find the time range during which the particles are most compact
start_time = 10000 # Start time varies, recommend starting with around 10000
end_time = 11000  # Adjust the end time as needed

best_time, min_area, best_bounding_box = find_minimum_area_time_range(particle_df, start_time, end_time)



# Now visualize the particles at the best time
final_pos, final_fig = create_message_grid(particle_df, best_time, True)
# final_fig.savefig("best_particle_positions.png")

print(f"Part 1: {final_fig}")
print(f"Part 2: Best time: {best_time}")
# print(f"Minimum bounding box area: {min_area}")
# print(f"Bounding box coordinates: {best_bounding_box}")