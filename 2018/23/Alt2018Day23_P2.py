# Advent of Code - Day 23, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/23
# Solution by: [abbasmoosajee07]
# Brief: [Tracking bots position, P2]
import  os, re
import pandas as pd
from collections import namedtuple

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

# Calculate the Manhattan distance between two points
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])

# Count how many nanobots are in range of a given point
def count_in_range(point, nanobots):
    count = 0
    for (x, y, z), r in nanobots:
        if manhattan_distance(point, (x, y, z)) <= r:
            count += 1
    return count

# Main function to find the point in range of the most nanobots
def find_best_point(df):
    check_distance = [0]
    # Extract nanobots from the DataFrame
    nanobots = [(tuple(row[['p_x', 'p_y', 'p_z']]), row['r']) for _, row in df.iterrows()]
    
    # Determine the bounds of the search space by looking at the ranges of nanobots
    x_min = min(x - r for (x, y, z), r in nanobots)
    x_max = max(x + r for (x, y, z), r in nanobots)
    y_min = min(y - r for (x, y, z), r in nanobots)
    y_max = max(y + r for (x, y, z), r in nanobots)
    z_min = min(z - r for (x, y, z), r in nanobots)
    z_max = max(z + r for (x, y, z), r in nanobots)

    # Search space with a step size to reduce computation (for simplicity, we're checking all points in range here)
    best_count = 0
    best_distance = float('inf')
    best_point = None

    # Iterate through the space
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            for z in range(z_min, z_max + 1):
                count = count_in_range((x, y, z), nanobots)
                if count > best_count or (count == best_count and manhattan_distance((x, y, z), (0, 0, 0)) < best_distance):
                    best_count = count
                    best_point = (x, y, z)
                    best_distance = manhattan_distance(best_point, (0, 0, 0))
                    check_distance.append(best_distance)
                    print(best_distance)
                    # if best_distance == check_distance[-1]:
                    #     break
                    
    return best_distance

# Parse the data into a DataFrame
input_pos_df = parse_particle_data(input_data)
# Find the best point and its Manhattan distance
result = find_best_point(input_pos_df)
# print("Best Manhattan distance:", result)
