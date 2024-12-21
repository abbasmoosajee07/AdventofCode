"""Advent of Code - Day 20, Year 2024
Solution Started: Dec 20, 2024
Puzzle Link: https://adventofcode.com/2024/day/20
Solution by: abbasmoosajee07
Brief: [Cheating in a race via teleportation]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from scipy.spatial import KDTree

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_grid(input_grid: list) -> tuple[set[tuple], tuple, tuple, tuple, set[tuple]]:
    walls = set()
    grid_bounds = (0, len(input_grid), 0, len(input_grid[0]))
    for row_no, row in enumerate(input_grid):
        # min_x, max_x, min_y, max_y
        for col_no, char in enumerate(row):
            if char == 'S':
                start = (row_no, col_no)
            elif char == 'E':
                goal = (row_no, col_no)
            elif char == '#':
                walls.add((row_no, col_no))
    return walls, start, goal, grid_bounds

def bfs_shortest_path(start: tuple, goal: tuple, walls: set[tuple], grid_bounds: tuple) -> tuple[dict, int]:
    min_x, max_x, min_y, max_y = grid_bounds
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # Up, Down, Right, Left

    queue = deque([start])
    visited = set([start])
    parent = {start: None}  # Track parent nodes
    path = {}
    while queue:
        current = queue.popleft()

        if current == goal:
            # Reconstruct path using parent mapping
            reconstructed_path = []
            while current:
                reconstructed_path.append(current)
                current = parent[current]
            reconstructed_path.reverse()  # Reverse to make the path go forward

            # Assign times in forward order
            for t, cell in enumerate(reconstructed_path, start=2):
                path[cell] = t - 1

            return path, len(reconstructed_path) - 1  # Path and travel_time

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if (
                min_x <= neighbor[0] < max_x and
                min_y <= neighbor[1] < max_y and
                neighbor not in walls and
                neighbor not in visited
            ):
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current  # Track the parent

    return None, -1  # No path found

def manhattan_distance(point_1: tuple, point_2: tuple) -> int:
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])

def test_cheat_codes(init_path: dict, cheat_code=2) -> int:
    pathway = list(init_path.keys())
    times = list(init_path.values())

    # Build a KDTree for efficient nearest-neighbor queries
    tree = KDTree(pathway)
    useful_cheats = 0

    for i, start in enumerate(pathway):
        # Query for all neighbors within cheat_code distance
        indices = tree.query_ball_point(start, cheat_code)
        for idx in indices:
            close = pathway[idx]
            abs_dist = manhattan_distance(start, close)
            if abs_dist <= cheat_code:
                open_portal = times[i]
                close_portal = init_path[close]
                time_diff = close_portal - open_portal - abs_dist
                if time_diff >= 100:
                    useful_cheats += 1
    return useful_cheats

walls, start, goal, grid_bounds = parse_grid(input_data)
base_path, full_time = bfs_shortest_path(start, goal, walls, grid_bounds)

if base_path:
    cheats_p1 = test_cheat_codes(base_path)
    print("Part 1:", cheats_p1)

    cheats_p2 = test_cheat_codes(base_path, 20)
    print("Part 2:", cheats_p2)
else:
    print("No valid path found.")