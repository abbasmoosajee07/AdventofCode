"""Advent of Code - Day 23, Year 2023
Solution Started: Jan 13, 2025
Puzzle Link: https://adventofcode.com/2023/day/23
Solution by: abbasmoosajee07
Brief: [Find Longest Path]
"""

#!/usr/bin/env python3

import os, re, copy, sys, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.setrecursionlimit(10**7)
start_time = time.time()

# Load the input data from the specified file path
D23_file = "Day23_input.txt"
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

# Read and sort input data into a grid
with open(D23_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_grid(init_grid: list) -> dict:
    grid_dict = {}
    start, goal = None, None
    # Iterate through the grid to update each tile to dict and update bounds
    for row_no, row in enumerate(init_grid):
        for col_no, tile in enumerate(row):
            grid_dict[(row_no, col_no)] = tile
            if tile == '.':
                goal = (row_no, col_no)
                if start is None:
                    start = (row_no, col_no)
    return grid_dict, start, goal

def print_grid(grid_dict: dict, movements: dict):
    min_row, min_col = min(grid_dict.keys())
    max_row, max_col = max(grid_dict.keys())

    grid_list = []

    for row_no in range(min_row, max_row + 1):
        row = ''
        for col_no in range(min_col, max_col + 1):
            pos = (row_no, col_no)

            if pos in movements:
                row += movements[pos]
            elif pos in grid_dict.keys():
                row += grid_dict[pos]
            else:
                row += '.'

        grid_list.append(row)

    # Print grid
    print("\nCurrent Grid:")
    for row in grid_list:
        print("".join(row))
    print()

def find_path_avoid_slopes(grid_dict: dict, start: tuple, goal: tuple) -> dict:
    def get_neighbors(pos: tuple):
        """Generate all valid neighboring positions and their directions."""
        row, col = pos
        for str_dir, (dr, dc) in DIRECTIONS.items():
            new_row, new_col = row + dr, col + dc
            new_pos = (new_row, new_col)
            if new_pos in grid_dict and grid_dict[new_pos] != '#':  # Ensure within bounds and not a wall
                yield new_pos, str_dir

    def dfs(current_pos, current_path):
        """Depth-first search to explore all paths."""
        nonlocal longest_path
        if current_pos == goal:
            # Update longest path if current path is longer
            if len(current_path) > len(longest_path):
                longest_path = current_path.copy()
            return

        # Check current position for slope logic
        if grid_dict[current_pos] in DIRECTIONS:
            slope_dir = grid_dict[current_pos]
            slope_dr, slope_dc = DIRECTIONS[slope_dir]
            slope_row, slope_col = current_pos[0] + slope_dr, current_pos[1] + slope_dc
            slope_pos = (slope_row, slope_col)
            if slope_pos not in current_path and slope_pos in grid_dict and grid_dict[slope_pos] != '#':
                current_path[slope_pos] = 'O'
                dfs(slope_pos, current_path)
                del current_path[slope_pos]  # Backtrack
            return  # No need to check normal neighbors if on a slope

        # Explore all normal neighbors
        for new_pos, str_dir in get_neighbors(current_pos):
            if new_pos not in current_path:  # Only visit unvisited positions
                current_path[new_pos] = 'O'
                dfs(new_pos, current_path)
                del current_path[new_pos]  # Backtrack

    # Define movement directions
    DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    longest_path = {}  # Store the longest path
    dfs(start, {start: 'S'})  # Start DFS with the initial position
    return longest_path

def find_longest_path(grid_dict: dict, start: tuple, goal: tuple) -> dict:
    def get_neighbors(init_pos: tuple):
        """Generate all valid neighboring positions based on slope logic."""
        if init_pos in neighbors_cache:
            return neighbors_cache[init_pos]

        init_row, init_col = init_pos
        neighbors = []  # Store valid neighbors and their directions
        for dir_char, (dr, dc) in DIRECTIONS.items():
            new_row, new_col = init_row + dr, init_col + dc
            new_pos = (new_row, new_col)
            if new_pos in grid_dict and grid_dict[new_pos] != '#':  # Valid position
                neighbors.append((new_pos, dir_char))

        neighbors_cache[init_pos] = neighbors
        return neighbors

    def dfs(current, path):
        nonlocal longest_path
        if current == goal:
            if len(path) > len(longest_path):
                longest_path = path[:]
            return

        for neighbor, dir_char in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append((neighbor, dir_char))
                dfs(neighbor, path)
                path.pop()  # Backtrack
                visited.remove(neighbor)

    # Define possible movement directions (cardinal directions)
    DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

    visited = {start}  # Track visited nodes
    longest_path = []  # Store the longest path as a list of (position, direction)
    neighbors_cache = {}  # Cache for neighbor computation
    dfs(start, [(start, 'S')])  # Mark the start point with 'S'

    # Convert the longest path back to a dictionary format
    return {pos: 'O' for pos, dir_char in longest_path}

test_input = ['#.#####################', '#.......#########...###', '#######.#########.#.###', '###.....#.>.>.###.#.###', '###v#####.#v#.###.#.###', '###.>...#.#.#.....#...#', '###v###.#.#.#########.#', '###...#.#.#.......#...#', '#####.#.#.#######.#.###', '#.....#.#.#.......#...#', '#.#####.#.#.#########v#', '#.#...#...#...###...>.#', '#.#.#v#######v###.###v#', '#...#.>.#...>.>.#.###.#', '#####v#.#.###v#.#.###.#', '#.....#...#...#.#.#...#', '#.#########.###.#.#.###', '#...###...#...#...#.###', '###.###.#.###v#####v###', '#...#...#.#.>.>.#.>.###', '#.###.###.#.###.#.#v###', '#.....###...###...#...#', '#####################.#']

grid_dict, start, goal = parse_grid(input_data)

path_p1 = find_path_avoid_slopes(grid_dict, start, goal)
print('Path 1:', len(path_p1) - 1)
print_grid(grid_dict, path_p1)

# path_p2 = find_longest_path(grid_dict, start, goal)
print('Path 2:', len(path_p2) - 1)
# print_grid(grid_dict, path_p2)


print(f"Execution Time = {time.time() - start_time:.5f}")
