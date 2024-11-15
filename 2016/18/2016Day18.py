# Advent of Code - Day 18, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/18
# Solution by: [abbasmoosajee07]
# Brief: [Identify Safe Tiles, based on past row]

import os
import numpy as np

# Example file name (adjust the path as needed)
D18_file = 'Day18_input.txt'
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Load the input
with open(D18_file_path) as file:
    input_data = file.read().strip()

# Count the number of safe tiles (zeros) in the entire room
def count_zeros_2d(arr):
    return np.sum(arr == 0)  # Efficiently count all zeros

# Parse input to a binary form where '^' is 1 (trap) and '.' is 0 (safe)
def parse_input(room_setup):
    room = []
    for trap_symbol in room_setup:
        if trap_symbol == "^":   # Trap Tile
            trap = 1
        elif trap_symbol == ".": # Safe Tile
            trap = 0
        room.append(trap)
    return np.array([room])

# Function to determine if the new tile is a trap based on surrounding tiles
def is_trap(left, center, right):
    if left == 1 and center == 1 and right == 0:
        return 1
    elif center == 1 and right == 1 and left == 0:
        return 1
    elif left == 1 and center == 0 and right == 0:
        return 1
    elif left == 0 and center == 0 and right == 1:
        return 1
    else:
        return 0


def extend_room(room_initial, input_data, room_extend):
    room = np.zeros((room_extend + 1, len(input_data)), dtype=int)  # Include space for all rows
    room[0] = room_initial  # First row is set

    # Build the room row by row based on the rules
    for row in range(room_extend):
        old_row = room[row]
        new_row = []
        for tile in range(len(old_row)):
            left = old_row[tile - 1] if tile > 0 else 0  # Assume safe if out of bounds
            center = old_row[tile]
            right = old_row[tile + 1] if tile < len(old_row) - 1 else 0  # Assume safe if out of bounds
            new_tile = is_trap(left, center, right)
            new_row.append(new_tile)
        
        room[row + 1] = new_row  # Set the new row into the room

    return room

# Define how many rows you want to compute

# Initialize the room with the initial input
room_initial = parse_input(input_data)

"""-------------------Part 1-----------------------"""
P1_extend = 40 - 1  # Adjust for how many rows you want, including the first one
P1_room = extend_room(room_initial, input_data, P1_extend)
P1_safe_tiles = count_zeros_2d(P1_room)
print(f"Part 1: Number of safe tiles: {P1_safe_tiles}")

"""-------------------Part 2-----------------------"""
P2_extend = 400000 - 1  # Adjust for how many rows you want, including the first one
P2_room = extend_room(room_initial, input_data, P2_extend)
P2_safe_tiles = count_zeros_2d(P2_room)
print(f"Part 2: Number of safe tiles: {P2_safe_tiles}")
