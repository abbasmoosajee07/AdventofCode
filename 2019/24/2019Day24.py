"""Advent of Code - Day 24, Year 2019
Solution Started: Mar 29, 2025
Puzzle Link: https://adventofcode.com/2019/day/24
Solution by: abbasmoosajee07
Brief: [Game of Life]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read and sort input data into a grid
with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n')

class Planet_Discord:
    def __init__(self):
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
                if state == '.':
                    if bugs in [1, 2]:
                        new_state = '#'
                elif state == '#':
                    if bugs == 1:
                        new_state = '#'
                new_row += new_state
            next_evolution.append(new_row)
        return '\n'.join(next_evolution)

    def calculate_biodiversity(self, planet_state: str) -> int:
        return sum(
            (2 ** index) if cell == '#' else 0
            for index, cell in enumerate("".join(planet_state.split('\n')))
        )

    def simulate_life(self, initial_state: list[str], visualize: bool = False):
        evolved_state = '\n'.join(initial_state)
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
                rating = self.calculate_biodiversity(evolved_state)
                break
            evolution_history[mins] = evolved_state
        return rating

test_input = ["....#", "#..#.", "#..##", "..#..", "#...."]

planet = Planet_Discord()
rating_p1 = planet.simulate_life(input_data)
print("Part 1:", rating_p1)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
