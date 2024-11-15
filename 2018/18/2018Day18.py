# Advent of Code - Day 18, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/18
# Solution by: [abbasmoosajee07]
# Brief: [Growing Sustainable Forests]

import os, re, copy
import numpy as np
import pandas as pd
from collections import defaultdict

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_data = [list(row) for row in input_data]
    input_grid = np.array(input_data)

# The lumber collection area is 50 acres by 50 acres;
# each acre can be either open ground (.), trees (|), or a lumberyard (#).

def find_nearby_acres(lumber_grid, x, y):
    # Define the directions of neighboring cells: 8 directions around (x, y)
    directions = [(-1, -1), (0, -1), (+1, -1),
                  (-1,  0),          (+1,  0),
                  (-1, +1), (0, +1), (+1, +1)]

    # Initialize the count dictionary
    land_counts = {'open_land': 0, 'lumberyard': 0, 'trees': 0}

    # Iterate through the 8 directions
    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        # Check if the neighbor is within bounds of the grid
        if 0 <= nx < len(lumber_grid) and 0 <= ny < len(lumber_grid[0]):
            # Add logic to check if it's a land type you're interested in, e.g., 'land'
            if lumber_grid[ny][nx] == '.':  # Check Open Ground
                land_counts['open_land'] += 1
            elif lumber_grid[ny][nx] == '|':  # Check Trees
                land_counts['trees'] += 1
            elif lumber_grid[ny][nx] == '#':  # Check Lumberyards
                land_counts['lumberyard'] += 1

    return land_counts

def update_grid(lumber_grid):
    # Create a copy of the grid to store updates
    updated_grid = np.copy(lumber_grid)

    # Iterate through the grid, checking each cell
    for y in range(len(lumber_grid)):
        for x in range(len(lumber_grid[y])):
            # Find nearby acres and store in a dictionary
            land_count = find_nearby_acres(lumber_grid, x, y)

            # Check Open Acre ('.') transformation
            if lumber_grid[y][x] == '.':
                if land_count['trees'] >= 3:
                    updated_grid[y][x] = '|'

            # Check Trees ('|') transformation
            elif lumber_grid[y][x] == '|':
                if land_count['lumberyard'] >= 3:
                    updated_grid[y][x] = '#'

            # Check Lumberyard ('#') transformation
            elif lumber_grid[y][x] == '#':
                if land_count['lumberyard'] >= 1 and land_count['trees'] >= 1:
                    updated_grid[y][x] = '#'
                else:
                    updated_grid[y][x] = '.'

    # Return the updated grid after the full iteration
    return updated_grid

def simulate_growth(grid, time):
    # Iterate through the grid update process for the given time
    
    resource_list = defaultdict(set,{})
    for mins in range(time):
        grid = update_grid(grid)
        # Count the number of trees ('|') and lumberyards ('#')
        trees = np.count_nonzero(grid == '|')
        lumber = np.count_nonzero(grid == '#')

        # Calculate the total value
        total_resources = trees * lumber
        # print(f"{mins}, {total_resources}")
        if total_resources in resource_list:
            if len(resource_list[total_resources]) > 3:
                period = mins - max(resource_list[total_resources])
                if (mins + 1) % period == 1000000000 % period:
                    break
        resource_list[total_resources].add(mins)
    return total_resources, resource_list

# Initialize grid
grid = input_grid

# Part 1
time_p1 = 10
P1_ans, _ = simulate_growth(input_grid, time_p1)
print(f"Part 1: Resources after {time_p1} is {P1_ans}")

# For example it produces zero, suggesting its not sustainable
time_p2 = 1000000000
P2_ans, _ = simulate_growth(input_grid, time_p2)
print(f"Part 2: Resources after {time_p2} is {P2_ans}")

