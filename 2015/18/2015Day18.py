# Advent of Code - Day 18, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/18
# Solution by: [abbasmoosajee07]
# Brief: [Game of Life Problem]

import os
import re
import copy
import numpy as np

D18_file = 'Day18_input.txt'
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

with open(D18_file_path) as file:
    lights_grid = file.read()

lights_grid = lights_grid.splitlines()

# print(lights_grid)

grid_x = len(lights_grid)
grid_y = grid_x
lights_matrix = np.zeros((grid_x, grid_y))


# Iterate through the whole apartment counting the floors as it goes along
for yn in range(grid_y):
    for xn in range(grid_x):
        light_n = lights_grid[yn][xn]
        if light_n == "#":
            lights_matrix[yn][xn] = 1
        else:
            lights_matrix[yn][xn] = 0
            
print(f"Number of lights originally on: {sum(sum(lights_matrix))}")

# Function to get the neighbors around a specific cell
def get_neighbors(array, i, j):
    rows = len(array)
    cols = len(array[0])
    
    # Possible directions (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
                  (0, -1),           (0, 1),     # left,       right
                  (1, -1), (1, 0), (1, 1)]     # bottom-left, bottom, bottom-right
    
    neighbors = []
    
    # Iterate through possible directions and check bounds
    for d in directions:
        new_i, new_j = i + d[0], j + d[1]
        if 0 <= new_i < rows and 0 <= new_j < cols:
            neighbors.append(array[new_i][new_j])
    
    return sum(neighbors)


def change_lights(lights_matrix_n):
    # Create a deep copy to avoid modifying the original matrix
    lights_copy = copy.deepcopy(lights_matrix_n)
    
    for yn in range(grid_y):
        for xn in range(grid_x):
            light_n = lights_matrix_n[yn][xn]
            neighbors_sum = get_neighbors(lights_matrix_n, yn, xn)  # Pass (yn, xn) to get_neighbors
            
            if light_n == 1:
                # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
                if neighbors_sum != 2 and neighbors_sum != 3:
                    lights_copy[yn][xn] = 0

            elif light_n == 0:
                # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
                if neighbors_sum == 3:
                    lights_copy[yn][xn] = 1
    
    return lights_copy


# Assuming grid_y and grid_x are the dimensions of the grid, and lights_matrix is initialized.
animations = 5
grid_n1 = lights_matrix  # Initial state of the lights grid
grid_n2 = lights_matrix  # Initial state of the lights grid

for step in range(animations):
    grid_n1 = change_lights(grid_n1)  # Apply the change_lights function at each step
    # print(grid_n1)

# Final state: sum the elements of the grid to see how many lights are on
print(f"Number of lights on after Part 1: {sum(sum(row) for row in grid_n1)}")

def corner_lights_on(lights_matrix_n):
    # Create a deep copy to avoid modifying the original matrix
    lights_copy = copy.deepcopy(lights_matrix_n)
    lights_copy[+0][+0] = 1
    lights_copy[+0][-1] = 1
    lights_copy[-1][+0] = 1
    lights_copy[-1][-1] = 1
    
    for yn in range(grid_y):
        for xn in range(grid_x):
            light_n = lights_matrix_n[yn][xn]
            neighbors_sum = get_neighbors(lights_matrix_n, yn, xn)  # Pass (yn, xn) to get_neighbors
            
            if light_n == 1:
                # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
                if neighbors_sum != 2 and neighbors_sum != 3:
                    lights_copy[yn][xn] = 0

            elif light_n == 0:
                # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
                if neighbors_sum == 3:
                    lights_copy[yn][xn] = 1
    
    lights_copy[+0][+0] = 1
    lights_copy[+0][-1] = 1
    lights_copy[-1][+0] = 1
    lights_copy[-1][-1] = 1                

                
    return lights_copy

for step in range(animations):
    grid_n2[+0][+0] = 1
    grid_n2[+0][-1] = 1
    grid_n2[-1][+0] = 1
    grid_n2[-1][-1] = 1
    grid_n2 = corner_lights_on(grid_n2)  # Apply the change_lights function at each step
    # print(grid_n2)

# Final state: sum the elements of the grid to see how many lights are on
print(f"Number of lights on after Part 1: {sum(sum(row) for row in grid_n2)}")
