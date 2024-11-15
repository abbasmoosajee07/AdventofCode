# Advent of Code - Day 12, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/12
# Solution by: [abbasmoosajee07]
# Brief: [Game of Life for Plants]

import os
import numpy as np

# Load the input data from the specified file path
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read input data
with open(D12_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_data):
    # Extract initial state and rules
    initial_state = input_data[0][len('initial state: '):]
    spread_notes = input_data[2:]

    # Convert spread rules into a set of patterns that produce a plant
    spread_list = set()
    for note in spread_notes:
        pattern, result = note.split(' => ')
        if result == '#':
            spread_list.add(pattern)

    # Initialize set of indices where plants are present in the initial state
    initial_state_set = set(i for i, pot in enumerate(initial_state) if pot == '#')

    return initial_state_set, spread_list

def next_generation(plant_row, spread_list):
    # Determine range of indices to consider in this generation
    start = min(plant_row) - 3
    end = max(plant_row) + 3

    # Set to store the indices of pots with plants for the next generation
    next_row = set()

    # Generate the next state by examining each pot index within the range
    for pot in range(start, end + 1):
        # Create a 5-character pattern centered on `pot`
        pot_str = ''.join('#' if (pot + k) in plant_row else '.' for k in [-2, -1, 0, 1, 2])
        if pot_str in spread_list:
            next_row.add(pot)  # Add pot to the next generation if the pattern matches a plant-producing rule

    return next_row

# Parse the initial state and spread rules
initial_state, spread_list = parse_input(input_data)

# Run simulation for 20 generations (Part 1)
def run_generations(spread_list, initial_state, generations):
    plant_grid = [initial_state]
    for generation in range(generations):
        cur_state = next_generation(plant_grid[-1], spread_list)
        plant_grid.append(cur_state)

    # Calculate the sum of plant pot indices for Part 1
    plant_count = sum(plant_grid[-1])
    return plant_count
plant_count_P1 = run_generations(spread_list, initial_state, 20)
print(f"Part 1: {plant_count_P1}")


# Part 2: Extrapolate to 50 billion generations
score199 = run_generations(spread_list, initial_state, 199)
score200 = run_generations(spread_list, initial_state, 200)
constantIncrease = score200 - score199
print('Part 2:', run_generations(spread_list, initial_state, 200) + ((50000000000 - 200) * constantIncrease))
