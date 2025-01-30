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
    """
    This class manages navigation for an Intcode-based vacuum robot within a scaffold maze.
    It provides functions to build the scaffold, identify intersections, find an optimal path,
    and control the vacuum robot based on computed path sequences.
    """
    def __init__(self, control_program: list[int], start_vac: tuple = None):
        from Intcode_Computer import Intcode_CPU
        self.DIRECTIONS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}  # Movement directions
        self.TURNS = {
            '^': {'<': 'L', '^': 1, '>': 'R'}, 'v': {'<': 'R', 'v': 1, '>': 'R'},
            '<': {'^': 'R', '<': 1, 'v': 'L'}, '>': {'^': 'L', '>': 1, 'v': 'R'}
        }
        self.MAX_LENGTH = 20
        self.navigator = Intcode_CPU(control_program)
        self.start_vac = [start_vac] if start_vac else []
        self.vacuum = Intcode_CPU(control_program)

        self.scaffold = None
        self.structure = None
        self.full_path = None
        self.intersections = None

    def get_next_position(self, base_pos: tuple, movement: int) -> tuple[int, int]:
        """
        Calculate the next position based on a movement direction.
        """
        x, y = base_pos
        dx, dy = self.DIRECTIONS[movement]
        return x + dx, y + dy

    def build_structure(self, nav_output: list[int] = None, visualize: bool = False):
        """
        Process navigation output and build the scaffold structure.
        Optionally visualize the maze.
        """
        if nav_output is None:
            self.navigator.process_program()
            nav_output = self.navigator.get_result('output')

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

    def identify_intersections(self, visualize: bool = False):
        """
        Identify intersections on the scaffold and optionally visualize them.
        """
        if self.scaffold is None:
            self.build_structure()

        intersections = set()
        for base_pos in self.scaffold:
            if all(self.get_next_position(base_pos, d)
                    in self.scaffold for d in self.DIRECTIONS):
                self.structure[base_pos] = 'O'
                intersections.add(base_pos)

        self.intersections = intersections

        if visualize:
            self.print_maze(self.structure)

        return intersections

    def identify_path(self, visualize: bool = False):
        """
        Identify instructions for the vacuum robot to navigate the scaffold path.
        """
        # Identify intersections on the scaffold
        if self.intersections is None:
            self.identify_intersections()

        # Initialize variables
        robot_path = {}  # Stores the robot's path with instructions
        visited = set()  # Tracks visited positions
        path_instructions = []  # Stores path instructions for the robot
        queue = [(self.robot_start, self.structure[self.robot_start])]  # BFS queue for robot movement

        while queue:
            current_pos, current_dir = queue.pop()

            # Attempt to move forward
            next_pos = self.get_next_position(current_pos, current_dir)
            if next_pos in self.scaffold and next_pos not in visited:
                if next_pos in self.intersections:
                    after_inter_pos = self.get_next_position(next_pos, current_dir)
                    robot_path[after_inter_pos] = current_dir
                    path_instructions[-1] += 2
                    queue.append((after_inter_pos, current_dir))
                    visited.add(after_inter_pos)
                else:
                    robot_path[next_pos] = current_dir
                    path_instructions[-1] += 1
                    queue.append((next_pos, current_dir))
                    visited.add(next_pos)
            else:
                # Explore all possible directions from the current position
                for test_dir, turn in self.TURNS.get(current_dir, {}).items():
                    test_pos = self.get_next_position(current_pos, test_dir)
                    if test_pos in self.scaffold and test_pos not in visited:
                        robot_path[current_pos] = turn
                        robot_path[test_pos] = test_dir
                        path_instructions.extend([turn, 1])
                        queue.append((test_pos, test_dir))
                        visited.add(test_pos)

        # Visualize the maze if requested
        if visualize:
            self.print_maze(self.structure, robot_path)

        self.full_path = [str(move) for move in path_instructions]
        return path_instructions

    def find_repeat(self, path: list[str], registers: list = [], sequence: list = []):
        """
        Find repeating path sequences that fit within register constraints.
        """
        # Base case: path cleared or registers fully allocated
        if not path:
            return (True, registers, sequence) if len(registers) <= 3 else (False, None, None)

        # Check if the path prefix matches any existing register
        for i, reg in enumerate(registers):
            if path[:len(reg)] == reg:
                return self.find_repeat(path[len(reg):], registers, sequence + [i])

        # Ensure no more than 3 registers are used
        if len(registers) == 3:
            return False, [], []

        # Determine the maximum allowable segment length
        register_len = min(len(path), self.MAX_LENGTH)

        # Backtrack and test different segment lengths
        while register_len > 0:
            segment = path[:register_len]
            if len(",".join(segment)) <= self.MAX_LENGTH and segment[-1] not in {'R', 'L'}:
                result, updated_registers, updated_sequence = self.find_repeat(
                    path[register_len:], registers + [segment], sequence + [len(registers)]
                )
                if result:
                    return result, updated_registers, updated_sequence
            register_len -= 1

        return False, [], []

    def drive_vacuum(self, func_list: list[str], main_func: str, visualize: bool = False):
        """
        Execute the vacuum program with provided functions and main sequence.
        Optionally visualize the process.
        """
        self.vacuum.edit_program(self.start_vac)
        commands = (
            [ord(char) for char in main_func] + [ord("\n")]
            + [ord(char) for char in func_list['A']] + [ord("\n")]
            + [ord(char) for char in func_list['B']] + [ord("\n")]
            + [ord(char) for char in func_list['C']] + [ord("\n")]
            + [ord("y") if visualize else ord("n"), ord("\n")]
        )
        all_commands = commands.copy()
        while commands:
            current_command = commands.pop(0)
            self.vacuum.paused = False
            self.vacuum.process_program(external_input=current_command)

            output = self.vacuum.get_result('output')
            if visualize:
                complete_list = output + all_commands
                self.build_structure(complete_list, visualize)

    def clean_structure(self, visualize: bool = False):
        """
        Clean the scaffold structure by identifying path and then running vacuum.
        """
        if self.structure is None:
            self.build_structure()
        if self.full_path is None:
            self.identify_path()

        _, registers, sequence = self.find_repeat(self.full_path)
        registers = {chr(65 + val): ','.join(registers[val]) for val in sequence}
        sequence = ','.join([chr(65 + val) for val in sequence])
        self.drive_vacuum(registers, sequence, visualize)
        return max(self.vacuum.get_result('output'))

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

navigator = Intcode_Navigators(input_program, start_vac = (0, 2))
intersections = navigator.identify_intersections()

alignment = sum(((x-1) * (y-1)) for (x, y) in intersections)
print("Part 1:", alignment)

dust_collected = navigator.clean_structure()
print("Part 2:", dust_collected)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
