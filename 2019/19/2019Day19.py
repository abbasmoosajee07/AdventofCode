"""Advent of Code - Day 19, Year 2019
Solution Started: Feb 4, 2025
Puzzle Link: https://adventofcode.com/2019/day/19
Solution by: abbasmoosajee07
Brief: [Intcode Drones]
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
D19_file = "Day19_input.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_Drones:
    def __init__(self, drone_program: list[int]):
        from Intcode_Computer import Intcode_CPU
        self.drone = Intcode_CPU(drone_program)

    def print_grid(self, grid_dict: dict):
        """
        Display the scanned grid in its current state
        """
        coords_set = set(grid_dict.keys())
        min_x = min(x for x, _ in coords_set)
        max_x = max(x for x, _ in coords_set)
        min_y = min(y for _, y in coords_set)
        max_y = max(y for _, y in coords_set)

        markers = {0:'.', 1:'#', 2: 'S'}

        tiles_grid = []
        for y in range(min_y, max_y + 1):
            row = ''
            for x in range(min_x, max_x + 1):
                row += markers.get(grid_dict.get((x, y), ' '),' ')

            tiles_grid.append(row)

        print("\n".join(tiles_grid))
        print("_" * len(tiles_grid[0]))
        return tiles_grid

    def is_in_beam(self, x: int, y: int) -> bool:
        """
        Check if a given coordinate is within the beam by querying the drone.
        """
        if x < 0 or y < 0:
            return False
        drone = self.drone.replicate()
        drone.process_program(external_input = [x, y])
        return drone.get_result('output')[-1] == 1

    def scan_area(self, scan_area: tuple[int, int], visualize: bool = False) -> int:
        """
        Scan the entire grid and count beam emissions.
        """
        width, height = scan_area
        beam_points = set()
        grid_dict = {(x, y) : 0 for x in range(width)
                                for y in range(height)}
        start_x = 0
        for y in range(height):
            beam_active = False
            start_x = max(0, start_x)

            for x in range(start_x, width):
                if self.is_in_beam(x, y):
                    if not beam_active:
                        start_x = x - 1  # Start scanning from slightly before the beam begins
                    beam_active = True
                    beam_points.add((x, y))
                    grid_dict[(x, y)] = 1
                elif beam_active:
                    # Stop scanning after the beam ends on this row
                    break

        if visualize:
            self.print_grid(grid_dict)

        return len(beam_points)

    def find_ship(self, ship_size: tuple[int, int], visualize: bool = False) -> tuple[int, int]:
        """
        Efficiently find the top-left corner of the ship that fits within the beam.
        """
        width, height = ship_size
        x_pos, y_pos = ship_size

        while True:
            # Skip unnecessary rows until bottom-right corner fits
            while not self.is_in_beam(x_pos + width - 1, y_pos):
                y_pos += 1

            # Skip unnecessary columns until top-left fits
            while not self.is_in_beam(x_pos, y_pos + height - 1):
                x_pos += 1

            # Check if the current (x, y) is a valid solution
            if self.is_in_beam(x_pos + width - 1, y_pos) and self.is_in_beam(x_pos, y_pos + height - 1):
                break

        if visualize:
            # Set up grid bounds around the ship for better visualization
            padding = 5
            grid_dict = {}

            for x in range(x_pos - padding, x_pos + width + padding):
                for y in range(y_pos - padding, y_pos + height + padding):
                    # Populate the grid with beam status
                    grid_dict[(x, y)] = 1 if self.is_in_beam(x, y) else 0

            # Mark ship corners
            for ship_y in range(y_pos, y_pos + height):
                for ship_x in range(x_pos, x_pos + width):
                    grid_dict[(ship_x, ship_y)] = 2

            # Print the grid
            self.print_grid(grid_dict)

        return x_pos, y_pos

drones = Intcode_Drones(input_program)
beam_shape = drones.scan_area((50, 50))
print("Part 1:", beam_shape)

ship_coord = drones.find_ship((100, 100))
print("Part 2:", (ship_coord[0] * 10000) + ship_coord[1])

# print(f"Execution Time = {time.time() - start_time:.5f}s")
