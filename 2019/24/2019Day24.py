"""Advent of Code - Day 24, Year 2019
Solution Started: Mar 29, 2025
Puzzle Link: https://adventofcode.com/2019/day/24
Solution by: abbasmoosajee07
Brief: [Game of Life]
"""

#!/usr/bin/env python3

import os, re, copy, time
from collections import Counter
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

    def evolve_infinite_system(self, current_state: dict):
        evolved_state = {}
        for (row, col, level), state in current_state.items():
            new_state, bugs_count = ['.', 0]
            if row == 0 or row == 4:
                
            for dr, dc in self.ADJACENT_POSITIONS:
                next_row, next_col = row + dr, col + dc
                
                if current_state.get((next_row, next_col, level), '.') == '#':
                    bugs_count += 1

            if state == '.' and bugs_count in [1, 2]:
                    new_state = '#'
            elif state == '#'and bugs_count == 1:
                    new_state = '#'
            evolved_state[(row, col, level)] = new_state
        print(evolved_state)
        return evolved_state

    def simulate_recursive_life(self, total_time: int, visualize: bool = False):
        mid = len(self.init_state) // 2
        init_recursion = [*self.init_state]
        init_recursion[mid] = init_recursion[mid][:mid] + '?' + init_recursion[mid][mid + 1:]

        BASE_GRID = ['.....', '.....', '..?..', '.....', '.....']
        life_state = {
            (row, col, 0): state
            for row, row_data in enumerate(init_recursion)
            for col, state in enumerate(row_data)
        }

        history = {0: Counter(life_state.values())['#']}
        for mins in range(1, total_time + 1):
            life_state = self.evolve_infinite_system(life_state)
            history[mins] = Counter(life_state.values())['#']

        return history


input_data = ['....#','#..#.','#..##','..#..','#....']

planet = Planet_Discord(input_data)
rating_p1 = planet.simulate_life()
print("Part 1:", rating_p1)

bug_history = planet.simulate_recursive_life(3)
print("Part 2:", bug_history)

print(f"Execution Time = {time.time() - start_time:.5f}s")

#      |     |         |     |
#   1  |  2  |    3    |  4  |  5
#      |     |         |     |
# -----+-----+---------+-----+-----
#      |     |         |     |
#   6  |  7  |    8    |  9  |  10
#      |     |         |     |
# -----+-----+---------+-----+-----
#      |     |A|B|C|D|E|     |
#      |     |-+-+-+-+-|     |
#      |     |F|G|H|I|J|     |
#      |     |-+-+-+-+-|     |
#  11  | 12  |K|L|?|N|O|  14 |  15
#      |     |-+-+-+-+-|     |
#      |     |P|Q|R|S|T|     |
#      |     |-+-+-+-+-|     |
#      |     |U|V|W|X|Y|     |
# -----+-----+---------+-----+-----
#      |     |         |     |
#  16  | 17  |    18   |  19 |  20
#      |     |         |     |
# -----+-----+---------+-----+-----
#      |     |         |     |
#  21  | 22  |    23   |  24 |  25
#      |     |         |     |
# Tile 19 has four adjacent tiles: 14, 18, 20, and 24.
# Tile G has four adjacent tiles: B, F, H, and L.
# Tile D has four adjacent tiles: 8, C, E, and I.
# Tile E has four adjacent tiles: 8, D, 14, and J.
# Tile 14 has eight adjacent tiles: 9, E, J, O, T, Y, 15, 19.
# Tile N has eight adjacent tiles: I, O, S, and
#   five tiles within the sub-grid marked ?.