"""Advent of Code - Day 15, Year 2019
Solution Started: Jan 26, 2025
Puzzle Link: https://adventofcode.com/2019/day/15
Solution by: abbasmoosajee07
Brief: [Intcode Maze Explorers]
"""

#!/usr/bin/env python3

import os, re, copy, sys, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

start_time = time.time()

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)
from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_Explorers:
    """
    A class to explore and map a maze using an Intcode CPU-based robot program.
    Includes functionality for maze mapping, shortest path finding, and flood filling.
    """

    def __init__(self, robot_program: list[int]):
        """
        Initialize the IntcodeExplorers instance with a robot program.
        """
        self.explorers = Intcode_CPU(robot_program, debug=False)
        self.DIRECTIONS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}  # Movement directions
        self.ROOM = {0: '#', 1: '.', 2: 'O'}  # Mapping for room statuses
        self.start_pos = (0, 0)

    def get_next_position(self, base_pos: tuple, movement: int) -> tuple[int, int]:
        """
        Calculate the next position based on a movement direction.
        """
        x, y = base_pos
        dx, dy = self.DIRECTIONS[movement]
        return x + dx, y + dy

    def map_maze(self, visualize: bool = False):
        """
        Explore and map the maze using the Intcode robot program.
        """
        check_queue = [(self.explorers, self.start_pos)]  # Queue for BFS exploration
        maze_dict = {self.start_pos: 'D'}  # Maze representation
        checked = set()  # Track visited positions

        while check_queue:
            cpu_state, current_pos = check_queue.pop(0)

            for test_dir in self.DIRECTIONS.keys():
                cpu_copy = cpu_state.replicate()
                cpu_copy.process_program(external_input=test_dir)
                new_pos = self.get_next_position(current_pos, test_dir)
                status_code = cpu_copy.get_result('output')[-1]
                cpu_copy.paused = False

                if new_pos not in maze_dict:
                    maze_dict[new_pos] = self.ROOM[status_code]

                if new_pos not in checked:
                    checked.add(new_pos)
                    if status_code == 1:  # Path continues
                        check_queue.append((cpu_copy, new_pos))
                    elif status_code == 2:  # Target found
                        self.goal = new_pos

        if visualize:
            self.print_maze(maze_dict)
        return maze_dict

    def find_shortest_path(self, grid_dict: dict, visualize: bool = False):
        """
        Find the shortest path from start to goal using BFS.
        """
        queue = [(self.start_pos, [self.start_pos])]  # BFS queue: (current position, path taken)
        visited = set([self.start_pos])  # Track visited cells

        while queue:
            current_pos, path = queue.pop(0)

            if current_pos == self.goal:
                return path

            for move in self.DIRECTIONS.keys():
                new_pos = self.get_next_position(current_pos, move)

                if grid_dict.get(new_pos, '#') != '#' and new_pos not in visited:
                    queue.append((new_pos, path + [new_pos]))
                    visited.add(new_pos)
                    if visualize:
                        print(f"Taken {len(path) - 1} steps:")
                        self.print_maze(grid_dict, path)

        return None  # No path exists

    def flood_fill(self, grid_dict: dict, visualize: bool = False):
        """
        Perform flood fill from the goal position to determine the time to fill the maze with oxygen.
        """
        oxygen_release = self.goal
        queue = [[oxygen_release]]  # Queue contains lists of positions at each level
        visited = {oxygen_release}  # Track visited cells
        mins = 0
        filled = []
        empty_space = set(coords for coords, space in grid_dict.items() if space == '.')

        while queue:
            mins += 1
            active_nodes = queue.pop(0)
            new_nodes = []

            for current_pos in active_nodes:
                for move in self.DIRECTIONS.keys():
                    new_pos = self.get_next_position(current_pos, move)

                    if grid_dict.get(new_pos, '#') == '.' and new_pos not in visited:
                        new_nodes.append(new_pos)
                        visited.add(new_pos)
                        filled.append(new_pos)

            if new_nodes:
                queue.append(new_nodes)
                if visualize:
                    print(f"After {mins} minutes")
                    self.print_maze(grid_dict, filled)

            if len(empty_space) == len(filled):
                break

        return mins

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
                if (x, y) == self.start_pos:
                    row += 'D'
                elif (x, y) == self.goal:
                    row += 'O'
                elif best_path and (x, y) in best_path:
                    row += '█' if '█'.encode().decode('utf-8', 'ignore') else '|'

                else:
                    row += grid_dict.get((x, y), ' ')
            tiles_grid.append(row)

        print("\n".join(tiles_grid))
        print("_" * len(tiles_grid))
        return tiles_grid

explorer_bots = Intcode_Explorers(input_program)
built_maze = explorer_bots.map_maze()

shortes_path = explorer_bots.find_shortest_path(built_maze)
print("Part 1:",len(shortes_path) - 1)

fill_time = explorer_bots.flood_fill(built_maze)
print("Part 2:", fill_time)

print(f"Execution Time = {time.time() - start_time:.5f}s")
