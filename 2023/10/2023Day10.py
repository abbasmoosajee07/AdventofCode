"""Advent of Code - Day 10, Year 2023
Solution Started: Dec 26, 2024
Puzzle Link: https://adventofcode.com/2023/day/10
Solution by: abbasmoosajee07
Brief: [Pipes and Loops]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()
# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read and sort input data into a grid
with open(D10_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_grid: list[str]) -> tuple[dict, tuple]:
    """Parse the grid input into a dictionary with start position identified."""
    grid_dict = {}
    start_pos = None
    for row_no, row in enumerate(input_grid):
        for col_no, char in enumerate(row):
            grid_dict[(row_no, col_no)] = char
            if char == 'S':  # Identify start position
                start_pos = (row_no, col_no)
    return grid_dict, start_pos


def print_grid(init_grid: list[str], loop_dict: dict):
    grid_print = []
    for row_no, row in enumerate(init_grid):
        print_row = ''
        for col_no, char in enumerate(row):
            if (row_no, col_no) in loop_dict.keys():
                print_row += loop_dict[(row_no, col_no)]
            else:
                print_row += char
        grid_print.append(print_row)

    for row in grid_print:
        print(row)


def identify_loop(grid_dict: dict, start_position: tuple) -> tuple[dict, int]:
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

    graph = {}
    loop_dict = {start_position:'S'}
    visited = set()

    # Build the graph from the grid dictionary
    for pos, tile in grid_dict.items():
        row, col = pos
        adjacent = []
        # Define valid moves based on tile type
        if tile in '-J7S':  # Can connect to the left
            adjacent.append((row, col - 1))
        if tile in '-FLS':  # Can connect to the right
            adjacent.append((row, col + 1))
        if tile in '|F7S':  # Can connect downward
            adjacent.append((row + 1, col))
        if tile in '|LJS':  # Can connect upward
            adjacent.append((row - 1, col))
        # Store the adjacent connections
        graph[(row, col)] = adjacent

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


grid_dict, start_pos = parse_input(input_data)
loop_path, steps = identify_loop(grid_dict, start_pos)
print("Part 1:", steps)

print(f"Execution Time: {time.time() - start_time:.5f}")

