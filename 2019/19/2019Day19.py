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
    def __init__(self, drone_program: list[str]):
        from Intcode_Computer import Intcode_CPU
        self.drone = Intcode_CPU
        self.drone_program = drone_program

    def run_scan(self, scan_area: tuple[int, int], visualize: bool = False) -> int:
        """
        Scan the entire grid and count beam emissions with optimizations.
        Assumes light proagates from single source, so once it ends stop counting for the row,
        and use the base point for previous row to start calculating
        """
        total_emissions = 0
        horizontal, vertical = scan_area
        grid_dict = {(x, y):0 for x in range(horizontal) for y in range(vertical)}
        min_x = 0

        for y in range(vertical):
            light_found = False
            for x in range(min_x, horizontal):
                # Initialize a new drone CPU for each scan
                drone = self.drone(self.drone_program, init_inputs=[x, y])
                drone.process_program()

                # Get the beam status output
                light_emitted = drone.get_result('output')[-1]
                grid_dict[(x, y)] = light_emitted

                if light_emitted == 1:
                    if light_found is False:
                        min_x = x - 1
                    light_found = True
                    total_emissions += 1
                elif light_found and light_emitted == 0:
                    # Stop scanning after the beam ends on this row
                    break

        # Visualize the grid if required
        if visualize:
            self.print_grid(grid_dict)

        return total_emissions

    def print_grid(self, grid_dict: dict):
        """
        Display the scanned grid in its current state
        """
        coords_set = set(grid_dict.keys())
        min_x = min(x for x, _ in coords_set)
        max_x = max(x for x, _ in coords_set)
        min_y = min(y for _, y in coords_set)
        max_y = max(y for _, y in coords_set)
        markers = {0:'.', 1:'#'}

        tiles_grid = []
        for y in range(min_y, max_y + 1):
            row = ''
            for x in range(min_x, max_x + 1):
                row += markers.get(grid_dict.get((x, y), ' '),' ')

            tiles_grid.append(row)

        print("\n".join(tiles_grid))
        print("_" * len(tiles_grid[0]))
        return tiles_grid


drones = Intcode_Drones(input_program)
beam_shape = drones.run_scan((50, 50))
print("Part 1:", beam_shape)


print(f"Execution Time = {time.time() - start_time:.5f}s")
