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
    def __init__(self, robot_program: list[int]):
        self.explorers = Intcode_CPU(robot_program, debug=False)
        self.DIRECTIONS = { 1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
        self.ROOM = {0:'#', 1:'.', 2: 'O'}
        self.start_pos = (0, 0)

    def get_next_position(self, base_pos: tuple, movement: int) -> tuple[int, int]:
        x, y = base_pos
        dx, dy = self.DIRECTIONS[movement]
        new_x, new_y = x + dx, y + dy
        return (new_x, new_y)

    def map_maze(self, show_maze: bool = False):
        """
        Processes the program for a given direction and calculates the next position.
        """
        check_queue = [(self.explorers, self.start_pos)]
        maze_dict = {self.start_pos: 'D'}
        checked = set()

        while check_queue:
            cpu_state, current_pos = check_queue.pop(0)

            for test_dir in list(self.DIRECTIONS.keys()):
                cpu_copy = cpu_state.replicate()
                cpu_copy.process_program(external_input=test_dir)
                new_pos = self.get_next_position(current_pos, test_dir)
                status_code = cpu_copy.get_result('output')[-1]
                cpu_copy.paused = False  # Ensure the CPU is ready for the next command

                if new_pos not in maze_dict:
                    maze_dict[new_pos] = self.ROOM[status_code]

                if new_pos not in checked:
                    checked.add(new_pos)  # Mark as visited
                    if status_code == 1:  # Path continues
                        check_queue.append((cpu_copy, new_pos))
                    elif status_code == 2:  # Target found (optional: handle if needed)
                        self.goal = new_pos

        if show_maze:
            self.print_maze(maze_dict)
        return maze_dict

    def find_shortest_path(self, grid_dict: dict):

        # BFS Initialization
        queue = [(self.start_pos, [self.start_pos])]  # (current position, path taken)
        visited = set([self.start_pos])            # Track visited cells

        while queue:
            current_pos, path = queue.pop()

            # Check if we've reached the goal
            if current_pos == self.goal:
                return path  # Return the full path

            # Explore neighbors in the four main directions(up, down, left, right)
            for move in list(self.DIRECTIONS.keys()):
                new_pos = self.get_next_position(current_pos, move)

                # Check if the next position is within bounds, traversable, and unvisited
                if (grid_dict.get(new_pos, 0)!= '#' and new_pos not in visited):
                    queue.append((new_pos, path + [new_pos]))  # Add the new position to the path
                    visited.add(new_pos)

        # If no path is found
        return None  # No path exists

    def print_maze(self, grid_dict: dict, best_path: list = None):
        """
        Displays the current state of the maze.
        """
        coords_set = set(grid_dict.keys())
        # Determine the bounds of the grid
        min_x = min(x for x, _ in coords_set)
        max_x = max(x for x, _ in coords_set)
        min_y = min(y for _, y in coords_set)
        max_y = max(y for _, y in coords_set)

        # Create the grid and print it
        tiles_grid = ["Intcode Maze"]
        for y in range(min_y, max_y + 1):  # Loop over rows (y-coordinates)
            row = ''
            for x in range(min_x, max_x + 1):  # Loop over columns (x-coordinates)
                if (x, y) == self.start_pos:
                    row += 'D'
                elif (x, y) == self.goal:
                    row += 'O'
                elif (x, y) in best_path:
                    row += '|'
                else:
                    row += grid_dict.get((x, y), ' ')  # Default to empty space
            tiles_grid.append(row)

        # Print the grid row by row
        print("\n".join(tiles_grid))
        print("_" * len(tiles_grid))  # Separator for each game frame
        return tiles_grid[1:]

explorer_bots = Intcode_Explorers(input_program)
maze = explorer_bots.map_maze()
path = explorer_bots.find_shortest_path(maze)
# explorer_bots.print_maze(maze, path)
print("Part 1:",len(path) - 1)
# print(f"Execution Time = {time.time() - start_time:.5f}s")

