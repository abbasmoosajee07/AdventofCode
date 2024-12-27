"""Advent of Code - Day 10, Year 2023
Solution Started: Dec 26, 2024
Puzzle Link: https://adventofcode.com/2023/day/10
Solution by: abbasmoosajee07
Brief: [Pipes and Loops]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read and sort input data into a grid
with open(D10_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_grid: list[str]) -> tuple[dict, dict, tuple]:
    """Parse the grid input into a dictionary with start position identified."""
    grid_dict = {}
    grid_graph = {}
    start_pos = None
    for row_no, row in enumerate(input_grid):
        for col_no, char in enumerate(row):
            grid_dict[(row_no, col_no)] = char
            adjacent = []
            if char in '-J7S':
                adjacent.append((row_no, col_no-1))
            if char in '-FLS':
                adjacent.append((row_no, col_no+1))
            if char in '|F7S':
                adjacent.append((row_no+1, col_no))
            if char in '|LJS':
                adjacent.append((row_no-1, col_no))
            if char == 'S':
                tile_q = set([(row_no, col_no)])
            grid_graph[(row_no, col_no)] = adjacent
            if char == 'S':  # Identify start position
                start_pos = (row_no, col_no)
    return grid_dict, grid_graph, start_pos

def print_grid(init_grid: list[str], loop_dict: dict, enclosed_area: set, filename: str):
    grid_print = []

    # Process the grid
    for row_no, row in enumerate(init_grid):
        print_row = ''
        for col_no, char in enumerate(row):
            if (row_no, col_no) in loop_dict.keys():
                print_row += loop_dict[(row_no, col_no)]
            elif (row_no, col_no) in enclosed_area:
                print_row += 'I'
            else:
                print_row += char
        grid_print.append(print_row)
    
    # Write to the text file
    with open(filename, 'w') as file:
        for row in grid_print:
            file.write(row + '\n')

    print(f"Grid printed to {filename}")

def identify_loop(grid_dict: dict, graph: dict,start_position: tuple) -> tuple[dict, int]:
    """
    Identifies the loop in the grid and tracks the directions taken at each step.

    Args:
        grid_dict (dict): The parsed grid as a dictionary of positions and tiles.
        start_position (tuple): The starting position in the grid.

    Returns:
        tuple: A dictionary of positions to directions and the total number of steps.
    """
    DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    PIPE_TYPE = {
        '|': {'^': '^', 'v': 'v'},      # Vertical pipe
        '-': {'>': '>', '<': '<'},      # Horizontal pipe
        'L': {'<': '^', 'v': '>'},      # Elbow L
        'J': {'>': '^', 'v': '<'},      # Elbow J
        '7': {'>': 'v', '^': '<'},      # Elbow 7
        'F': {'^': '>', '<': 'v'},      # Elbow F
        'S': {'^': '^', 'v': 'v', '<': '<', '>': '>'}  # Starting point
    }

    loop_dict = {start_position:'S'}
    visited = set()

    # Initialize BFS from the start position
    visited.add(start_position)
    q = set([start_position])
    steps = -1  # Count the number of steps

    # BFS to find the furthest point and track directions
    while q:
        nxt = set()
        for current_row, current_col in q:
            for next_row, next_col in graph.get((current_row, current_col), []):
                # Ensure bidirectional connection is valid
                if (next_row, next_col) not in visited and (current_row, current_col) in graph.get((next_row, next_col), []):
                    # Determine the new direction
                    row_diff, col_diff = next_row - current_row, next_col - current_col
                    for dir_key, (dr, dc) in DIRECTIONS.items():
                        if (row_diff, col_diff) == (dr, dc):
                            new_direction = PIPE_TYPE[grid_dict[(next_row, next_col)]].get(dir_key, '?')
                            break
                    else:
                        new_direction = '?'

                    nxt.add((next_row, next_col))
                    visited.add((next_row, next_col))
                    loop_dict[(next_row, next_col)] = new_direction  # Track the direction
        q = nxt
        steps += 1
    loop_dict[(next_row, next_col)] = 'X'
    return loop_dict, steps

def find_enclosed_area(graph: dict, loop_path: dict) -> int:
    """Calculate the enclosed area inside a loop in the grid."""

    # Collect all pipes in the graph
    pipes = set()
    for row_1, col_1 in loop_path:
        for row_2, col_2 in graph[(row_1, col_1)]:
            # Check for bidirectional connection in the graph
            if (row_1, col_1) in graph.get((row_2, col_2), []):
                pipe = (*sorted((row_1, row_2)), *sorted((col_1, col_2)))
                pipes.add(pipe)

    ROW_LEN, COL_LEN = max(set(graph.keys()))
    visited = set()
    corner_q = [(0, 0)]

    while corner_q:
        i, j = corner_q.pop()
        requirements = (i > 0, j < COL_LEN, i < ROW_LEN, j > 0)
        adjacent = ((i-1, j), (i, j+1), (i+1, j), (i, j-1))
        tile_pairs = ((i-1, i-1, j-1, j),     # up
                        (i-1, i, j, j),       # right
                        (i, i, j-1, j),       # down
                        (i-1, i, j-1, j-1))   # left
        for req, corner, tile_pair in zip(requirements, adjacent, tile_pairs):
            if req and corner not in visited and tile_pair not in pipes:
                visited.add(corner)
                corner_q.append(corner)

    enclosed_area = set()
    for i, j in graph.keys():
            corners = ((i, j), (i+1, j), (i, j+1), (i+1, j+1))
            if not any(c in visited for c in corners):
                enclosed_area.add((i,j))
    return enclosed_area

grid_dict, graph, start_pos = parse_input(input_data)
loop_path, steps = identify_loop(grid_dict, graph, start_pos)
enclosed_area = find_enclosed_area(graph, loop_path)
print("Part 1:", steps)
print("Part 2:", len(enclosed_area))

# print_grid(input_data, loop_path, enclosed_area, 'pipe_maze.txt')

