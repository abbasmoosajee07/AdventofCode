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

class Intcode_Painters:
    """
    Simulates a painting robot controlled by an Intcode program.
    The robot moves on a grid, paints tiles based on the program's outputs, 
    and changes its direction accordingly.
    """
    def __init__(self, robot_program: list[int], start_pos: tuple = ((0, 0), '^')):
        """
        Initialize the painting robot with its program and starting position.
        """
        # Directions and turning logic
        self.DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
        self.TURNS = {
            0: {'^': '<', '<': 'v', 'v': '>', '>': '^'},  # Turn left
            1: {'^': '>', '>': 'v', 'v': '<', '<': '^'}   # Turn right
        }
        self.start_pos = start_pos
        from Intcode_Computer import Intcode_CPU
        self.painter = Intcode_CPU(robot_program)

    def run_robot(self, base_color: int) -> tuple[dict, int]:
        """
        Simulates the robot painting operation using a base color of 0 or 1.
        """
        current_pos, current_dir = self.start_pos
        tiles = {current_pos: base_color}  # Track tile colors
        painted_tiles = 1  # Count unique tiles painted at least once

        while self.painter.running:
            # Get current tile color, defaulting to black (0)
            current_color = tiles.get(current_pos, 0)

            # Process program with current tile color as input
            self.painter.process_program(external_input=current_color)
            outputs = self.painter.get_result('output')[-2:]  # Paint and turn outputs

            if len(outputs) < 2:
                raise ValueError('Fewer than 2 outputs returned')

            paint_color, turn_dir = outputs

            # Paint the current tile and count new tiles
            if (current_pos not in tiles) and (paint_color == 1):
                painted_tiles += 1
            tiles[current_pos] = paint_color

            # Update direction and position
            current_dir = self.TURNS[turn_dir][current_dir]
            dx, dy = self.DIRECTIONS[current_dir]
            current_pos = (current_pos[0] + dx, current_pos[1] + dy)

            self.painter.paused = False  # Resume the CPU

        return tiles, painted_tiles

    def print_grid(self, painted_tiles: dict):
        """
        Prints the painted grid to the console.
        """
        # Determine grid boundaries
        min_x = min(x for x, _ in painted_tiles)
        max_x = max(x for x, _ in painted_tiles)
        min_y = min(y for _, y in painted_tiles)
        max_y = max(y for _, y in painted_tiles)

        # Build and display the grid
        for x in range(min_x, max_x + 1):
            row = ''.join('|' if painted_tiles.get((x, y), 0) == 1 else ' ' 
                            for y in range(min_y, max_y + 1))
            print(row)

# Part 1: Run the robot starting with black (0)
painting_robots = Intcode_Painters(input_program)
_, painted = painting_robots.run_robot(0)
print("Part 1:", painted)

# Part 2: Run the robot starting with white (1)
painters_p2 = Intcode_Painters(input_program)
tiles_p2, _ = painters_p2.run_robot(1)
print("Part 2:---------------------------------")
painters_p2.print_grid(tiles_p2)
