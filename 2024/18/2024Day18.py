"""Advent of Code - Day 18, Year 2024
Solution Started: Dec 18, 2024
Puzzle Link: https://adventofcode.com/2024/day/18
Solution by: abbasmoosajee07
Brief: [Path Finder in a Grid]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
start_time = time.time()
# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')
    all_walls =   [(int(coords.split(',')[0]),
                    int(coords.split(',')[1])) for coords in input_data]

def get_grid_bounds(walls):

    if not walls:
        return (0, 0, 0, 0)  # Default if no walls exist

    x_coords = [x for x, y in walls]
    y_coords = [y for x, y in walls]

    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    return (min_x, max_x, min_y, max_y), (min_x, min_y), (max_x, max_y)

def bfs_shortest_path(start, target, walls, grid_bounds):

    min_x, max_x, min_y, max_y = grid_bounds
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left

    # Check if start or target is a wall
    if start in walls or target in walls:
        return -1

    # Initialize BFS
    queue = deque([(start, 0)])  # (current_position, steps)
    visited = set()
    visited.add(start)

    # BFS loop
    while queue:
        current, steps = queue.popleft()

        # Check if we reached the target
        if current == target:
            return steps, True

        # Explore neighbors
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if (
                min_x <= neighbor[0] <= max_x and  # Stay within x bounds
                min_y <= neighbor[1] <= max_y and  # Stay within y bounds
                neighbor not in walls and         # Avoid walls
                neighbor not in visited           # Avoid revisiting
            ):
                queue.append((neighbor, steps + 1))
                visited.add(neighbor)

    # If we exhaust the queue, no path exists
    return -1, False

def find_blocking_wall(start, target, walls, grid_bounds):

    # Copy walls to simulate adding them incrementally
    incremental_walls = set()
    for wall in walls:
        # Add the wall incrementally
        incremental_walls.add(wall)
        
        # Check if the path is still reachable
        _, wall_reached = bfs_shortest_path(start, target, incremental_walls, grid_bounds)
        if not wall_reached:
            return wall  # Return the first wall that blocks the path

    # If all walls are added and the path is never blocked
    return None

walls_p1 = all_walls[:1024]
walls_p2 = all_walls  # Walls to simulate
grid_bounds, start, goal = get_grid_bounds(all_walls)

# Call BFS
shortest_path_length, _ = bfs_shortest_path(start, goal, walls_p1, grid_bounds)
print(f"Part 1: {shortest_path_length}")

# Find the first blocking wall
blocking_wall = find_blocking_wall(start, goal, walls_p2, grid_bounds)
print(f"Part 2: {blocking_wall}")
print(time.time()-start_time)
