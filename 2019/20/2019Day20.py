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
    DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    PATH_MARKER = '█' if '█'.encode().decode('utf-8', 'ignore') else '|'

    def __init__(self, maze_grid: list[str]):
        self.maze_grid = maze_grid
        self.portals, self.grid_dict = {}, {}
        self.maze_size = (len(maze_grid), len(maze_grid[0]))
        self.parse_grid()

    def parse_grid(self):
        """
        Parse the maze to extract walls, paths, and portals.
        """
        self.BASE_MAZE = {(row, col): cell for row, row_data in enumerate(self.maze_grid)
                for col, cell in enumerate(row_data)}

        for (row, col), cell in self.BASE_MAZE.items():
            if cell.isupper():
                # Detect vertical and horizontal portal labels
                self.__detect_portals(self.BASE_MAZE, row, col)

            if cell in ['.', '#']:
                self.grid_dict[(row, col)] = cell

    def __detect_portals(self, grid, row, col):
        """
        Helper method to detect and classify portal locations.
        """
        height, width = self.maze_size

        if grid.get((row + 1, col), '0').isupper():  # Vertical portal
            portal_name = grid[row, col] + grid[row + 1, col]
            if row > 0 and grid.get((row - 1, col), '0') == '.':
                self.portals.setdefault(portal_name, []).append((row - 1, col))
            elif row < height - 2 and grid.get((row + 2, col), '0') == '.':
                self.portals.setdefault(portal_name, []).append((row + 2, col))

        if grid.get((row, col + 1), '0').isupper():  # Horizontal portal
            portal_name = grid[row, col] + grid[row, col + 1]
            if col > 0 and grid.get((row, col - 1), '0') == '.':
                self.portals.setdefault(portal_name, []).append((row, col - 1))
            elif col < width - 2 and grid.get((row, col + 2), '0') == '.':
                self.portals.setdefault(portal_name, []).append((row, col + 2))

    def print_maze(self, best_path: list, base_grid: dict = {}, visualize: bool = True):
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
                    cell = self.PATH_MARKER
                else:
                    cell = grid_dict.get((row_no, col_no), ' ')
                row += cell
            tiles_grid.append(row)
        if visualize:
            print("\n".join(tiles_grid))
            print("_" * len(tiles_grid[0]))
        return tiles_grid

    def get_next_position(self, base_pos: tuple[int, int], movement: str) -> tuple[int, int]:
        row, col = base_pos
        dr, dc = self.DIRECTIONS[movement]
        return row + dr, col + dc

    def traverse_maze(self, start_gate: str, goal_gate: str, visualize: bool = False) -> int:
        """
        Find the shortest path between start and goal gates using BFS.
        """
        start_pos = self.portals[start_gate][0]
        queue = [(start_pos, 0, [start_pos])]  # (position, steps, path)
        visited = set()
        min_steps = float('inf')

        while queue:
            current_pos, steps, path = queue.pop(0)
            if current_pos == self.portals[goal_gate][0] and steps < min_steps:
                min_steps = steps
                if visualize:
                    print(f" Shortest Path found with {steps} steps:")
                    self.print_maze(path)

            # Explore neighbors
            for move in self.DIRECTIONS.keys():
                next_pos = self.get_next_position(current_pos, move)
                if next_pos not in visited and self.grid_dict.get(next_pos) == '.':
                    visited.add(next_pos)
                    queue.append((next_pos, steps + 1, path + [next_pos]))

            # Handle portal teleportation
            for portal_name, positions in self.portals.items():
                if current_pos in positions:
                    for portal_exit in positions:
                        if portal_exit != current_pos and portal_exit not in visited:
                            visited.add(portal_exit)
                            queue.append((portal_exit, steps + 1, path + [portal_exit]))

                            # Visualization step at each portal
                            if visualize:
                                print(f"Teleport through {portal_name} | Total {steps + 1} steps:")
                                self.print_maze(path + [next_pos, portal_exit])
                            break
        return min_steps

    def traverse_recursive_graph(self, start_gate: str, goal_gate: str, visualize: bool = False) -> int:
        """
        Find the shortest path from start_gate to goal_gate using BFS with recursive level traversal.
        """
        grid = self.BASE_MAZE
        maze_height, maze_width = self.maze_size
        portal_positions = self.portals

        # Initialize BFS queue and visited set
        start_pos = portal_positions[start_gate][0]
        target_pos = portal_positions[goal_gate][0]
        queue = [(start_pos, 0, 0, start_gate)]  # (position, recursion_level, distance)
        visited = set([(start_pos, 0)])  # (col, row, recursion_level)

        while queue:
            (current_row, current_col), recursion_level, distance, previous_portal = queue.pop(0)

            # Check if we've reached the target on the base level
            if (current_row, current_col) == target_pos and recursion_level == 0:
                return distance

            # Explore all possible moves
            for (delta_row, delta_col) in self.DIRECTIONS.values():
                next_row, next_col = current_row + delta_row, current_col + delta_col
                new_recursion_level = recursion_level
                portal_name = None
                # Handle portal transitions
                if grid.get((next_row, next_col), '0').isupper():
                    is_outer_portal = (
                        next_col == 1 or next_row == 1 or
                        next_col == maze_width - 2 or next_row == maze_height - 2
                    )
                    new_recursion_level = recursion_level - 1 if is_outer_portal else recursion_level + 1

                    # Determine portal name by reading two adjacent uppercase cells
                    portal_name = (
                        grid.get((min(next_row, next_row + delta_row), min(next_col, next_col + delta_col)), '0') +
                        grid.get((max(next_row, next_row + delta_row), max(next_col, next_col + delta_col)), '0')
                    )

                    # Skip invalid portals or recursion level violations
                    if portal_name not in ('AA', 'ZZ') and new_recursion_level >= 0:
                        if (current_row, current_col) == portal_positions[portal_name][0]:
                            next_row, next_col = portal_positions[portal_name][1]
                        else:
                            next_row, next_col = portal_positions[portal_name][0]

                        if visualize:
                            if previous_portal != portal_name:
                                print(f"Walk from {previous_portal} to {portal_name} ({distance} step{'s' if distance - 1 > 1 else ''})")
                                print(f"From level {recursion_level}, Recurse to level {new_recursion_level} through {portal_name} ({distance} step{'s' if distance - 1 > 1 else ''})")

                # Skip already visited states
                if (next_row, next_col, new_recursion_level) in visited:
                    continue
                else:
                    visited.add((next_row, next_col, new_recursion_level))

                # Continue BFS only on valid paths
                if grid.get((next_row, next_col), '0') == '.':
                    queue.append(((next_row, next_col), new_recursion_level, distance + 1, previous_portal if portal_name is None else portal_name))

        # Return -1 if no valid path is found
        return -1

donuts = DonutMaze(input_data)

maze_path = donuts.traverse_maze('AA', 'ZZ')
print("Part 1:", maze_path)

recursion_path = donuts.traverse_recursive_graph('AA', 'ZZ')
print("Part 2:", recursion_path)

print(f"Execution Time = {time.time() - start_time:.5f}s")
