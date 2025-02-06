"""Advent of Code - Day 20, Year 2019
Solution Started: Feb 5, 2025
Puzzle Link: https://adventofcode.com/2019/day/20
Solution by: abbasmoosajee07
Brief: [Maze and Portals]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()
# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    input_data = file.read().split('\n')

class DonutMaze:
    def __init__(self, maze_grid: list[str]):
        self.DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
        self.path_marker = '█' if '█'.encode().decode('utf-8', 'ignore') else '|'

        self.parse_grid(maze_grid)

    def get_next_position(self, base_pos: tuple, movement: str) -> tuple[int, int]:
        """
        Calculate the next position based on a movement direction.
        """
        row, col = base_pos
        dr, dc = self.DIRECTIONS[movement]
        return row + dr, col + dc

    def parse_grid(self, input_grid: list[str]):
        grid_dict, portals = {}, {}
        visited = set()
        init_grid = {(row, col): cell for row, row_data in enumerate(input_grid)
                        for col, cell in enumerate(row_data) if cell != ' '}

        for pos, cell in init_grid.items():
            if cell in ['#', '.'] and pos not in visited:
                grid_dict[pos] = cell
            if cell == '.' and pos not in visited:
                letter_sequence = []
                sequence_positions = {pos}
                visited.add(pos)

                # Check all four directions to find letter sequences
                for direction in self.DIRECTIONS.keys():
                    current_pos = self.get_next_position(pos, direction)
                    while current_pos in init_grid and init_grid[current_pos].isalpha():
                        letter_sequence.append(init_grid[current_pos])
                        sequence_positions.add(current_pos)
                        visited.add(current_pos)
                        current_pos = self.get_next_position(current_pos, direction)

                if letter_sequence:
                    portal_name = ''.join(sorted(letter_sequence))
                    grid_dict[pos] = portal_name
                    if portal_name not in portals:
                        portals[portal_name] = []
                    portals[portal_name].append(pos)
                    for sequence_pos in sequence_positions:
                        visited.add(sequence_pos)

        self.BASE_MAZE = init_grid
        self.maze_dict = grid_dict
        self.portals = portals

        return grid_dict, portals

    def traverse_maze(self, start_gate: str, goal_gate: str, visualize: bool = False) -> tuple[list[tuple[int, int]], int]:
        """
        Find the shortest path from start_gate to goal_gate using BFS.
        """
        start_pos = self.portals[start_gate][0]
        goal_pos = self.portals[goal_gate][0]
        queue = [(start_pos, [start_pos])]  # (current position, path)
        visited = {start_pos}
        portal_names = set(self.portals.keys())

        while queue:
            current_pos, path = queue.pop(0)

            # Check if goal is reached
            if current_pos == goal_pos:
                if visualize:
                    print(f"Path found with {len(path)} steps:")
                    self.print_maze(path)
                return path, len(path)

            # Explore neighbors
            for move in self.DIRECTIONS.keys():
                next_pos = self.get_next_position(current_pos, move)
                next_cell = self.maze_dict.get(next_pos, '#')

                if next_pos not in visited:
                    # Handle regular path
                    if next_cell == '.' or next_pos == goal_pos:
                        queue.append((next_pos, path + [next_pos]))
                        visited.add(next_pos)

                    # Handle portal traversal
                    elif next_cell in portal_names:
                        point_1, point_2 = self.portals[next_cell]
                        portal_exit = point_2 if next_pos == point_1 else point_1
                        queue.append((portal_exit, path + [next_pos, portal_exit]))
                        visited.update([next_pos, portal_exit])
                        # Visualization step at each portal
                        if visualize:
                            print(f"After {len(path)} steps:")
                            self.print_maze(path + [next_pos, portal_exit])
        # Return empty result if no path is found
        return [], -1

    def print_maze(self, best_path: list, base_grid: dict = {}):
        """
        Display the maze with the current state, optionally highlighting a path.
        """
        grid_dict = base_grid or self.BASE_MAZE
        coords_set = set(grid_dict.keys())
        min_col = min(col for _, col in coords_set)
        max_col = max(col for _, col in coords_set)
        min_row = min(row for row, _ in coords_set)
        max_row = max(row for row, _ in coords_set)

        tiles_grid = []
        for row_no in range(min_row, max_row + 1):
            row = ''
            for col_no in range(min_col, max_col + 1):
                if (row_no, col_no) in best_path:
                    cell = self.path_marker
                else:
                    cell = grid_dict.get((row_no, col_no), ' ')
                row += cell
            tiles_grid.append(row)

        print("\n".join(tiles_grid))
        print("_" * len(tiles_grid[0]))
        return tiles_grid

donuts = DonutMaze(input_data)
shortest_path, fewest_steps = donuts.traverse_maze('AA', 'ZZ')
print("Part 1:", fewest_steps - 1)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
