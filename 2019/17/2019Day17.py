"""Advent of Code - Day 17, Year 2019
Solution Started: Jan 29, 2025
Puzzle Link: https://adventofcode.com/2019/day/17
Solution by: abbasmoosajee07
Brief: [Intcode Navigators]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)
# from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_Navigators:
    def __init__(self, control_program: list[int]):
        from Intcode_Computer import Intcode_CPU
        self.navigator = Intcode_CPU(control_program)
        self.DIRECTIONS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}  # Movement directions

    def get_next_position(self, base_pos: tuple, movement: int) -> tuple[int, int]:
        """
        Calculate the next position based on a movement direction.
        """
        x, y = base_pos
        dx, dy = self.DIRECTIONS[movement]
        return x + dx, y + dy

    def build_scaffold(self, visualize: bool = False):
        self.navigator.process_program()
        nav_output = self.navigator.get_result('output')

        x, y = (1, 1)
        structure = {}
        scaffold = set()
        for ascii_code in nav_output:
            x += 1
            if ascii_code == 10:
                y += 1
                x = 0
            else:
                structure[(x, y)] = chr(ascii_code)
                if chr(ascii_code) in '^v<>':
                    self.robot_start = (x, y)
                if ascii_code == 35:
                    scaffold.add((x,y))

        if visualize:
            self.print_maze(structure)

        self.structure = structure
        self.scaffold = scaffold
        return structure

    def identify_intersections(self, visualize: bool = False):
        intersections = set()
        for base_pos in self.scaffold:
            surrounding = 0
            for test_dir in list(self.DIRECTIONS.keys()):
                next_pos = self.get_next_position(base_pos, test_dir)
                if next_pos in self.scaffold:
                    surrounding += 1
                else:
                    break
            if surrounding == 4:
                self.structure[base_pos] = 'O'
                intersections.add(base_pos)

        if visualize:
            self.print_maze(self.structure)

        return intersections

    def print_maze(self, grid_dict: dict, best_path: list = None):
        """
        Display the maze with the current state, optionally highlighting a path.
        """
        coords_set = set(grid_dict.keys())
        min_x = min(x for x, _ in coords_set)
        max_x = max(x for x, _ in coords_set)
        min_y = min(y for _, y in coords_set)
        max_y = max(y for _, y in coords_set)

        tiles_grid = []
        for y in range(min_y, max_y + 1):
            row = ''
            for x in range(min_x, max_x + 1):
                row += grid_dict.get((x, y), ' ')
                # row += '█' if '█'.encode().decode('utf-8', 'ignore') else '|'

            tiles_grid.append(row)

        print("\n".join(tiles_grid))
        print("_" * len(tiles_grid[0]))
        return tiles_grid

navigator = Intcode_Navigators(input_program)
scaffold = navigator.build_scaffold()

intersections = navigator.identify_intersections()
alignment = sum(((x-1) * (y-1)) for (x, y) in intersections)
print("Part 1:", alignment)


print(f"Execution Time = {time.time() - start_time:.5f}s")
