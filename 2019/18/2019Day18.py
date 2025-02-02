"""Advent of Code - Day 18, Year 2019
Solution Started: Jan 30, 2025
Puzzle Link: https://adventofcode.com/2019/day/18
Solution by: abbasmoosajee07
Brief: [Breaking a Vault]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')

class TritonVault:
    def __init__(self, blueprints: list[str]):
        self.blueprint = blueprints
        self.path_marker = '█' if '█'.encode().decode('utf-8', 'ignore') else '|'
        self.DIRECTIONS = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}

        # Initialize grid attributes
        self.start_pos = None
        self.WALLS = set()
        self.passage = set()
        self.DOORS_KEYS = {}
        self.BASE_VAULT = {}
        self.TARGETS = {}
        self.overall_path = {}
        self.parse_grid(blueprints)

    def parse_grid(self, vault: list[str] = None):
        """
        Parse the grid from blueprint and identify special elements.
        """
        vault = vault or self.blueprint

        for row_no, row in enumerate(vault):
            for col_no, tile in enumerate(row):
                pos = (row_no, col_no)
                self.BASE_VAULT[pos] = tile

                if tile == '@':  # Starting position
                    self.start_pos = pos
                    self.TARGETS[pos] = tile
                    self.BASE_VAULT[pos] = '.'

                elif tile == '#':  # Wall
                    self.WALLS.add(pos)

                elif tile == '.':  # Passage
                    self.passage.add(pos)

                else:  # Doors or Keys
                    self.DOORS_KEYS[tile] = pos
                    self.TARGETS[pos] = tile

    def get_next_position(self, init_pos: tuple[int, int], move: str) -> tuple[int, int]:
        """
        Return the next position based on the current position and direction.
        """
        dr, dc = self.DIRECTIONS[move]
        return init_pos[0] + dr, init_pos[1] + dc

    def print_maze(self, path_taken: dict = {}):
        """
        Display the maze with path visualization.
        """
        min_row = min(row for row, _ in self.WALLS)
        max_row = max(row for row, _ in self.WALLS)
        min_col = min(col for _, col in self.WALLS)
        max_col = max(col for _, col in self.WALLS)

        vault_grid = []

        for row_no in range(min_row, max_row + 1):
            row = ''
            for col_no in range(min_col, max_col + 1):
                pos = (row_no, col_no)
                if pos in self.WALLS:
                    tile = '#'
                elif pos in path_taken:
                    tile = path_taken[pos]
                else:
                    tile = self.TARGETS.get(pos, '.')
                row += tile
            vault_grid.append(row)

        print("\n".join(vault_grid))
        print("_" * (max_col - min_col + 1))

    def map_path(self, visualize: bool = False) -> int:
        """
        Map and visualize the shortest path from the start to collect all keys using BFS.
        """
        from collections import deque
        # Initialize BFS queue: (steps, current_pos, collected_keys_bitmask)
        queue = deque([(0, self.start_pos, 0)])

        # Compute the bitmask for all keys
        all_keys_bitmask = (1 << len([k for k in self.DOORS_KEYS if k.islower()])) - 1

        # Visited states to avoid redundant exploration
        visited = set()
        overall_path = {}

        while queue:
            steps, current_pos, collected_keys = queue.popleft()

            # Return if all keys are collected
            if collected_keys == all_keys_bitmask:
                return steps

            # Skip already visited states with the same keys
            state = (current_pos, collected_keys)
            if state in visited:
                continue
            visited.add(state)

            # Explore all adjacent positions
            for direction in self.DIRECTIONS:
                next_pos = self.get_next_position(current_pos, direction)

                # Skip walls
                if next_pos in self.WALLS:
                    continue

                tile = self.BASE_VAULT.get(next_pos, '.')

                # Handle doors
                if tile.isupper() and not (collected_keys & (1 << (ord(tile.lower()) - ord('a')))):
                    continue  # Door is locked, skip this path

                # Handle keys
                new_collected_keys = collected_keys
                if tile.islower():
                    new_collected_keys |= (1 << (ord(tile) - ord('a')))

                # Add the new state to the queue
                queue.append((steps + 1, next_pos, new_collected_keys))
                overall_path[next_pos] = direction #self.path_marker

                if visualize:
                    print(f"Move to {next_pos} with steps: {steps + 1}, keys: {bin(new_collected_keys)}")
                    self.print_maze(overall_path)

        print("No valid path found.")
        return -1

vault = TritonVault(input_data)
steps = vault.map_path()
print("Part 1:", (steps))

# print(f"Execution Time: {time.time() - start_time}")