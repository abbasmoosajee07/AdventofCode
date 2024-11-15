# Advent of Code - Day 13, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/13
# Solution by: [abbasmoosajee07]
# Brief: [Breadth Find Search problem]

import os
import numpy as np
from collections import deque


D13_file = 'Day13_input.txt'
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

# Read input file
with open(D13_file_path) as file:
    input_no = file.read().splitlines()

def identify_system_space(x, y, fav_no):
    design_eq = (x*x) + (3*x) + (2*x*y) + (y) + (y*y)
    total_val = fav_no + design_eq
    binary_rep = bin(total_val)
    bit_sum = binary_rep.count('1')
    if bit_sum  % 2 == 0:
    # If the number of bits that are 1 is even, it's an open space. "."
        space_type = "."
    else:
    # If the number of bits that are 1 is odd, it's a wall. "#"
        space_type = "#"
    
    # print([xn,yn,design_eq,fav_no,total_val,binary_rep,bit_sum,space_type])
       
    return space_type

# Create a 3x4 zero matrix
rows, cols = 50, 50
zero_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

fav_no = int(input_no[0])

for yn in range(rows):
    for xn in range(cols):
        # space_xy = zero_matrix[xn][yn]
        
        space_xy = identify_system_space(xn, yn, fav_no)
        zero_matrix[yn][xn] = space_xy
    
grid = zero_matrix
# Define possible movements (up, down, left, right)
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (dy, dx)

"""-----------------------------------Part 1---------------------------------------"""
def is_valid1(y, x, visited):
    return (0 <= y < len(grid)) and (0 <= x < len(grid[0])) and (grid[y][x] == '.') and not visited[y][x]

def bfs1(start, goal):
    count = 0
    queue = deque([start])
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    visited[start[0]][start[1]] = True
    parent = {start: None}  # To reconstruct the path

    while queue:
        current = queue.popleft()
        
        # If we reached the goal, reconstruct the path
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Return reversed path

        for dy, dx in moves:
            next_y, next_x = current[0] + dy, current[1] + dx
            count += 1
            if is_valid1(next_y, next_x, visited):
                visited[next_y][next_x] = True
                queue.append((next_y, next_x))
                parent[(next_y, next_x)] = current        
    return None  # No path found

# Define start and goal positions (you can modify these)
start = (1, 1)    # Starting point (row, column)
goal = (39, 31)   # Goal point (row, column)

# Find the shortest path
shortest_path = bfs1(start, goal)
# Find the shortest path
shortest_path = bfs1(start, goal)

# Check if a path was found
if shortest_path is not None:
    print(f"Part 1: To reach goal coordinates of {goal}, {len(shortest_path) - 1} steps are required.")
else:
    print(f"Part 1: No path found to reach goal coordinates {goal}.")

"""-----------------------------------Part 2---------------------------------------"""
def is_valid2(y, x, visited):
    # Check if the position is within the grid and if it is a valid path and not visited
    return (0 <= y < len(grid)) and (0 <= x < len(grid[0])) and (grid[y][x] == '.') and ((y, x) not in visited)

def bfs2(start, max_steps):
    queue = deque([(start, 0)])  # (current position, current step count)
    visited = set()  # To track distinct positions visited
    visited.add(start)

    while queue:
        current, steps = queue.popleft()

        # If the maximum steps are reached, do not explore further
        if steps < max_steps:
            for dy, dx in moves:
                next_y, next_x = current[0] + dy, current[1] + dx
                if is_valid2(next_y, next_x, visited):
                    visited.add((next_y, next_x))  # Add the valid position to the visited set
                    queue.append(((next_y, next_x), steps + 1))

    return visited  # Return all distinct positions visited

# Define starting position and maximum steps
max_steps = 50   # Maximum number of steps allowed

# Find distinct locations that can be visited
distinct_locations = bfs2(start, max_steps)

# Output the result
print(f"Part 2: Distinct locations that can be visited within {max_steps} steps: {len(distinct_locations)}")
# print("Locations:", distinct_locations)