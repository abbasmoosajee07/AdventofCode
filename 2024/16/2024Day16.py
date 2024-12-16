"""Advent of Code - Day 16, Year 2024
Solution Started: Dec 16, 2024
Puzzle Link: https://adventofcode.com/2024/day/16
Solution by: abbasmoosajee07
Brief: [Path finder in  a maze]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heapq

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input):
    map_grid = np.array([list(row) for row in input], dtype = object)
    for row_no, row in enumerate(map_grid):
        for col_no, char in enumerate(row):
            if char == 'S':
                start = (row_no, col_no)
            if char == 'E':
                end = (row_no, col_no)
    return map_grid, start, end

def path_finder(grid, start, goal):
    DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left

    rows, cols = len(grid), len(grid[0])  # Grid dimensions

    optimal_tiles = []  # To track the tiles in the optimal path
    visited = set()  # To track the visited nodes
    heapq.heappush(optimal_tiles, (0, start[0], start[1], 1))  # Start by facing right (east)
    start_to_goal_dist = {}  # Store the minimum distance from start to each tile
    best_path_cost = None  # To track the best path cost

    # First A* search: from start to goal
    while optimal_tiles:
        current_cost, r, c, direction = heapq.heappop(optimal_tiles)

        if (r, c, direction) not in start_to_goal_dist:
            start_to_goal_dist[(r, c, direction)] = current_cost

        if (r, c) == goal and best_path_cost is None:
            best_path_cost = current_cost

        if (r, c, direction) in visited:
            continue
        visited.add((r, c, direction))

        dr, dc = DIRECTIONS[direction]
        next_r, next_c = r + dr, c + dc

        if 0 <= next_c < cols and 0 <= next_r < rows and grid[next_r][next_c] != '#':
            heapq.heappush(optimal_tiles, (current_cost + 1, next_r, next_c, direction))

        # Allow for direction changes (turning left or right)
        heapq.heappush(optimal_tiles, (current_cost + 1000, r, c, (direction + 1) % 4))
        heapq.heappush(optimal_tiles, (current_cost + 1000, r, c, (direction + 3) % 4))

    optimal_tiles = []  # Reset for second search
    visited = set()  # Reset visited set
    goal_to_start_dist = {}  # To store the minimum distance from goal to each tile

    # Start a second A* search: from goal to start (going backwards)
    for direction in range(4):
        heapq.heappush(optimal_tiles, (0, goal[0], goal[1], direction))

    while optimal_tiles:
        current_cost, r, c, direction = heapq.heappop(optimal_tiles)

        if (r, c, direction) not in goal_to_start_dist:
            goal_to_start_dist[(r, c, direction)] = current_cost

        if (r, c, direction) in visited:
            continue
        visited.add((r, c, direction))

        # Going backwards (reverse the direction)
        dr, dc = DIRECTIONS[(direction + 2) % 4]
        next_r, next_c = r + dr, c + dc

        if 0 <= next_c < cols and 0 <= next_r < rows and grid[next_r][next_c] != '#':
            heapq.heappush(optimal_tiles, (current_cost + 1, next_r, next_c, direction))

        # Allow for direction changes (turning left or right)
        heapq.heappush(optimal_tiles, (current_cost + 1000, r, c, (direction + 1) % 4))
        heapq.heappush(optimal_tiles, (current_cost + 1000, r, c, (direction + 3) % 4))

    # Now calculate the optimal tiles: those whose start-to-goal and goal-to-start distances sum to the best path cost
    optimal_tiles_set = set()  # Set to store the optimal tiles
    for r in range(rows):
        for c in range(cols):
            for direction in range(4):
                # A tile (r, c, direction) is part of the optimal path if the sum of the distances equals the best cost
                if (r, c, direction) in start_to_goal_dist and (r, c, direction) in goal_to_start_dist:
                    if start_to_goal_dist[(r, c, direction)] + goal_to_start_dist[(r, c, direction)] == best_path_cost:
                        optimal_tiles_set.add((r, c))

    return optimal_tiles_set, best_path_cost

grid, start, goal = parse_input(input_data)

# Run A* search
path, cost = path_finder(grid, start, goal)

# Print results
if path:
    print("Part 1:", cost)
    print("Part 2:", len(path))
else:
    print("No path found.")
