"""Advent of Code - Day 11, Year 2019
Solution Started: Jan 23, 2025
Puzzle Link: https://adventofcode.com/2019/day/11
Solution by: abbasmoosajee07
Brief: [Intcode Painting Robots]
"""

#!/usr/bin/env python3

import os, re, copy, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)

from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = list(map(int, input_data))

def run_robot(robot_program: list[int], base_color: int) -> tuple[dict, int]:
    """
    Simulates a robot painting operation using the given Intcode program.

    Args:
        robot_program (list[int]): The Intcode program to run the robot.
        base_color (int): Initial color of the base tile (0 for black, 1 for white).

    Returns:
        tuple: A dictionary of tile positions and their final colors,
                and the number of tiles painted at least once.
    """
    # Direction vectors and turning logic
    DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    TURNS = {
        0: {'^': '<', '<': 'v', 'v': '>', '>': '^'},  # Turn left
        1: {'^': '>', '>': 'v', 'v': '<', '<': '^'}   # Turn right
    }

    # Initialize robot state
    current_pos = (0, 0)
    current_dir = '^'
    tiles = {current_pos: base_color}  # Dictionary to store tile colors
    painted_tiles = 1  # Tracks the number of tiles painted at least once

    # Initialize Intcode CPU
    robot_cpu = Intcode_CPU(robot_program)

    while robot_cpu.running:
        # Get current tile color (default to 0 if unpainted)
        current_color = tiles.get(current_pos, 0)

        # Provide input to CPU and run the program
        robot_cpu.process_program(external_input=current_color)
        outputs = robot_cpu.get_result('output')[-2:]  # Get the latest paint and turn commands

        if len(outputs) < 2:  # Ensure both outputs are available
            break

        paint_color, turn_dir = outputs

        # Paint the current tile
        if current_pos not in tiles and paint_color == 1:  # Increment counter if painting a new tile
            painted_tiles += 1

        tiles[current_pos] = paint_color

        # Update the robot's direction and position
        current_dir = TURNS[turn_dir][current_dir]
        dx, dy = DIRECTIONS[current_dir]
        current_pos = (current_pos[0] + dx, current_pos[1] + dy)

        robot_cpu.paused = False  # Resume the CPU for the next cycle

    return tiles, painted_tiles

def print_grid(painted_tiles: dict):
    tiles_grid = []
    # Determine the bounds of the grid
    min_x = min(pos[0] for pos in painted_tiles)
    max_x = max(pos[0] for pos in painted_tiles)
    min_y = min(pos[1] for pos in painted_tiles)
    max_y = max(pos[1] for pos in painted_tiles)

    # Create and print the grid
    for x in range(min_x, max_x + 1):
        row = ''
        for y in range(min_y, max_y + 1):
            color = painted_tiles.get((x, y), 0)  # Default to black if not in the grid
            row += '|' if color == 1 else ' '  # Use █ for white and space for black
        tiles_grid.append(row)

    for row in tiles_grid:
        print(row)

_, painted = run_robot(input_program, 0)
print("Part 1:", painted)

tiles_p2, _ = run_robot(input_program, 1)
print("Part 2:---------------------------------")
print_grid(tiles_p2)