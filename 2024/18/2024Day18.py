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
            return visited, steps

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
    return -1, 0

def find_blocking_wall(start, target, walls, grid_bounds, min_check = 1024):
    # Add the first min walls initially
    incremental_walls = set(walls[:min_check])

    # Define a helper function to check if a wall blocks the path
    def is_path_blocked(wall_index):
        # Add all walls up to the current index
        current_walls = incremental_walls | set(walls[min_check:wall_index + 1])
        _, wall_reached = bfs_shortest_path(start, target, current_walls, grid_bounds)
        return wall_reached == 0

    # Perform binary search on the remaining walls
    left, right = min_check, len(walls) - 1
    blocking_wall = None

    while left <= right:
        mid = (left + right) // 2

        if is_path_blocked(mid):
            # If the path is blocked, this is a potential candidate
            blocking_wall = walls[mid]
            # Narrow the search to earlier walls
            right = mid - 1
        else:
            # Otherwise, search in the later walls
            left = mid + 1

    return blocking_wall  # Return the first blocking wall found, or None if no wall blocks the path

walls_p1 = all_walls[:1024]

walls_p2 = all_walls  # Walls to simulate
grid_bounds, start, goal = get_grid_bounds(all_walls)

# Call BFS
_, shortest_path_length = bfs_shortest_path(start, goal, walls_p1, grid_bounds)
print(f"Part 1: {(shortest_path_length)}")




# Find the first blocking wall
blocking_wall = find_blocking_wall(start, goal, walls_p2, grid_bounds)
print(f"Part 2: {blocking_wall}")
print(time.time()-start_time)
