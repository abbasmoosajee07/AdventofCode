# Advent of Code - Day 6, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/6
# Solution by: [abbasmoosajee07]
# Brief: [Marked Point Map]

import os
import numpy as np
from collections import defaultdict, deque

# Load the input data from the specified file path
D6_file = "Day06_input.txt"
D6_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D6_file)

# Read and sort input data into a grid
with open(D6_file_path) as file:
    input_data = file.read().strip().split('\n')

def create_grid(coords_data, size=1000):
    # Initialize a grid of the given size with None
    coord_grid = np.full((size, size), None)
    coordinates = []

    for line in coords_data:
        x, y = map(int, line.split(', '))
        coordinates.append((x, y))
        coord_grid[y][x] = (x, y)  # Store the coordinate in the grid

    return coordinates, coord_grid

def calculate_distances(coord_grid, coordinates):
    size = coord_grid.shape[0]
    distance_grid = [[[] for _ in range(size)] for _ in range(size)]  # Initialize distance grid with empty lists
    area_counts = defaultdict(int)
    infinite_coords = set()

    for y in range(size):
        for x in range(size):
            min_distance = float('inf')
            closest_coord = None
            closest_letter = None
            multiple_closest = False

            for i, (coord_x, coord_y) in enumerate(coordinates):
                distance = abs(coord_x - x) + abs(coord_y - y)

                if distance < min_distance:
                    min_distance = distance
                    closest_coord = i
                    closest_letter = chr(ord('A') + closest_coord)  # Map to letters A, B, C, ...
                    multiple_closest = False
                elif distance == min_distance:
                    multiple_closest = True
            
            if multiple_closest:
                continue  # No single closest coordinate
            
            # Store the closest letter and the distance in the distance_grid
            distance_grid[y][x] = [closest_letter.lower(), min_distance]
            
            area_counts[closest_coord] += 1
            
            # Check if this coordinate touches the edges
            if x == 0 or x == size - 1 or y == 0 or y == size - 1:
                infinite_coords.add(closest_coord)

    return distance_grid, area_counts, infinite_coords

def calculate_safe_region_size(coordinates, threshold=100):
    size = 1000  # Define grid size
    safe_region_size = 0

    # Iterate through the grid to calculate distances
    for y in range(size):
        for x in range(size):
            total_distance = 0
            
            for coord_x, coord_y in coordinates:
                # Calculate Manhattan distance
                distance = abs(coord_x - x) + abs(coord_y - y)
                total_distance += distance
            
            # Check if the total distance is within the threshold
            if total_distance < threshold:
                safe_region_size += 1

    return safe_region_size

# Run the solution using the defined functions
coordinates, coord_grid = create_grid(input_data)
distance_grid, area_counts, infinite_coords = calculate_distances(coord_grid, coordinates)

# Remove counts of infinite areas
for coord in infinite_coords:
    if coord in area_counts:
        del area_counts[coord]

# Find the largest finite area
largest_finite_area = max(area_counts.values(), default=0)

# Print the results
print(f"The size of the largest finite area is: {largest_finite_area}")

safe_region_size = calculate_safe_region_size(coordinates, threshold=10000)
print(f"The size of the safe region is: {safe_region_size}")

# Print the distance grid for debugging
# for row in distance_grid:
#     print(row)
