"""Advent of Code - Day 24, Year 2019
Solution Started: Mar 29, 2025
Puzzle Link: https://adventofcode.com/2019/day/24
Solution by: abbasmoosajee07
Brief: [Game of Life]
"""

#!/usr/bin/env python3

import os, re, copy, time
from collections import Counter
from collections import defaultdict
start_time = time.time()

# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read and sort input data into a grid
with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n')

class Planet_Discord:
    def __init__(self, initial_state: list[str]):
        self.init_state = initial_state
        self.grid_size = len(initial_state)
        self.ADJACENT_POSITIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def get_adjacent_bug_count(self, position: tuple, state_dict: dict) -> int:
        row, col = position
        return sum(
            state_dict.get((row + dr, col + dc), '.') == '#'
            for dr, dc in self.ADJACENT_POSITIONS
        )

    def evolve_life(self, current_state: list[str]) -> list[str]:
        state_matrix = current_state.split('\n')
        state_dict = {(row, col): state
                        for (row, row_data) in enumerate(state_matrix)
                        for (col, state) in enumerate(row_data)}
        next_evolution = []

        for (row, row_data) in enumerate(state_matrix):
            new_row = ""
            for (col, state) in enumerate(row_data):
                new_state = '.'
                bugs = self.get_adjacent_bug_count((row, col), state_dict)
                if state == '.' and bugs in [1, 2]:
                        new_state = '#'
                elif state == '#'and bugs == 1:
                        new_state = '#'
                new_row += new_state
            next_evolution.append(new_row)
        return '\n'.join(next_evolution)

    def simulate_life(self, visualize: bool = False):
        evolved_state = '\n'.join(self.init_state)
        mins = 0
        evolution_history = {0: evolved_state}
        if visualize:
            print(f"Initial State:\n{evolved_state}")
        while True:
            mins += 1
            evolved_state = self.evolve_life(evolved_state)
            if visualize:
                print(f"After {mins} minute:\n{evolved_state}")
            if evolved_state in evolution_history.values():
                rating = sum(
                    (2 ** index) if cell == '#' else 0
                    for index, cell in enumerate("".join(evolved_state.split('\n')))
                )
                break
            evolution_history[mins] = evolved_state
        return rating

    def get_adjacent_recursive(self, x: int, y: int, z: int):
        """Returns the list of adjacent coordinates, accounting for recursion."""
        if (x, y) == (2, 2):  # The center square leads to recursion.
            return []

        adjacent = []

        # Left
        if x == 0:
            adjacent.append((1, 2, z - 1))  # Outward recursion
        elif (x, y) == (3, 2):
            adjacent.extend((4, yy, z + 1) for yy in range(self.grid_size))  # Inward recursion
        else:
            adjacent.append((x - 1, y, z))

        # Right
        if x == 4:
            adjacent.append((3, 2, z - 1))
        elif (x, y) == (1, 2):
            adjacent.extend((0, yy, z + 1) for yy in range(self.grid_size))
        else:
            adjacent.append((x + 1, y, z))

        # Up
        if y == 0:
            adjacent.append((2, 1, z - 1))
        elif (x, y) == (2, 3):
            adjacent.extend((xx, 4, z + 1) for xx in range(self.grid_size))
        else:
            adjacent.append((x, y - 1, z))

        # Down
        if y == 4:
            adjacent.append((2, 3, z - 1))
        elif (x, y) == (2, 1):
            adjacent.extend((xx, 0, z + 1) for xx in range(self.grid_size))
        else:
            adjacent.append((x, y + 1, z))

        return adjacent

    def count_adjacent_bugs(self, grids, x, y, z):
        """Counts the number of adjacent bugs for a given cell."""
        adjacent = self.get_adjacent_recursive(x, y, z)
        ch = grids[z][y][x]
        n_neighbours = 0
        for x, y, z in adjacent:
            if z not in grids and ch != "#":
                continue
            if grids[z][y][x] == "#":
                n_neighbours += 1
        return n_neighbours

    def evolve_cell(self, grids, x, y, z):
        """Determines the next state of a cell based on the number of adjacent bugs."""
        bug_neighbors = self.count_adjacent_bugs(grids, x, y, z)
        if grids[z][y][x] == "#":
            return "#" if bug_neighbors == 1 else "."
        return "#" if bug_neighbors in (1, 2) else "."

    def evolve_level(self, grids, z):
        """Evolves an entire grid level for the next iteration."""
        return tuple(
            tuple(self.evolve_cell(grids, x, y, z) for x in range(self.grid_size))
            for y in range(self.grid_size)
        )

    def empty_grid(self):
        """Returns an empty grid."""
        return tuple(tuple("." for _ in range(5)) for _ in range(5))

    def iterate(self, grids):
        """Evolves all active grid levels, including newly created levels if necessary."""
        new_grids = defaultdict(self.empty_grid)
        grids_to_scan = set(grids)
        for z in grids_to_scan:
            new_grids[z] = self.evolve_level(grids, z)
        for z in set(grids) - grids_to_scan:
            new_grids[z] = self.evolve_level(grids, z)
        return new_grids

    def count_bugs(self, grids: list) -> int:
        return sum(ch == "#" for grid in grids.values() for line in grid for ch in line)

    def simulate_recursive_bugs(self, total_time: int, visualize: bool = False) -> dict:
        """Simulates the recursive bug evolution using a grid-based approach."""
        grid = tuple(tuple(ch for ch in line) for line in self.init_state)
        grids = defaultdict(self.empty_grid, {0: grid})

        history = {0: self.count_bugs(grids)}
        for mins in range(1, total_time + 1):
            grids = self.iterate(grids)
            bug_count = self.count_bugs(grids)
            history[mins] = bug_count
            if visualize:
                print(f"{mins=}, size={len(grids)}, bug_count={bug_count}")

        return history

planet = Planet_Discord(input_data)
rating_p1 = planet.simulate_life()
print("Part 1:", rating_p1)

full_time = 200
bug_history = planet.simulate_recursive_bugs(full_time)
print("Part 2:", bug_history[full_time])

# print(f"Execution Time = {time.time() - start_time:.5f}s")


