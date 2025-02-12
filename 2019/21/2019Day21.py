"""Advent of Code - Day 21, Year 2019
Solution Started: Feb 11, 2025
Puzzle Link: https://adventofcode.com/2019/day/21
Solution by: abbasmoosajee07
Brief: [Intcode Springdroid]
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
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_Springdroid:
    MAX_MEMORY = 15

    def __init__(self, springscript: list[int]):
        self.script = springscript
        self.temp_val = False
        self.jump_val = False
        from Intcode_Computer import Intcode_CPU
        self.droid = Intcode_CPU(springscript, debug = False)

    def run_droids(self, script: str, visualize: bool = False):
        inp_list = [ord(val) for val in list(script)]
        use_droid = self.droid.replicate()
        for num in inp_list:
            use_droid.paused = False
            use_droid.process_program(external_input = num)
            if visualize:
                self.build_structure(use_droid.get_result('output')[:-1], True)
        output = use_droid.get_result('output')
        return max(output)

    def build_structure(self, nav_output: list[int] = None, visualize: bool = False):
        """
        Process navigation output and build the ship hull.
        Optionally visualize the maze.
        """
        x, y = 1, 1
        structure = {}
        scaffold = set()
        for ascii_code in nav_output:
            if ascii_code == 10:
                y += 1
                x = 0
            else:
                char = chr(ascii_code)
                structure[(x, y)] = char
                if char in '^v<>':
                    self.robot_start = (x, y)
                if char == '#':
                    scaffold.add((x, y))
            x += 1

        if visualize:
            self.print_maze(structure)

        self.structure = structure
        self.scaffold = scaffold
        return structure

    def print_maze(self, grid_dict: dict, path_taken: dict = {}):
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
                if (x, y) in path_taken:
                    row += path_taken.get((x, y), ' ')
                else:
                    row += grid_dict.get((x, y), ' ')

            tiles_grid.append(row)

        print("\n".join(tiles_grid))
        print("_" * len(tiles_grid[0]))
        return tiles_grid

walk_script = """\
    NOT A J
    NOT B T
    OR T J
    NOT C T
    OR T J
    AND D J
    WALK
    """

run_script ="""\
    NOT A J
    NOT B T
    OR T J
    NOT C T
    OR T J
    AND D J
    NOT H T
    NOT T T
    OR E T
    AND T J
    RUN
    """

springs = Intcode_Springdroid(input_program)
walk_score = springs.run_droids(walk_script)
print("Part 1:", walk_score)

run_score = springs.run_droids(run_script)
print("Part 2:", run_score)
# print(f"\nExecution Time: {time.time() - start_time:.5f}s")
# print(f"Execution Time = {time.time() - start_time:.5f}s")
