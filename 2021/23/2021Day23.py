# Advent of Code - Day 23, Year 2021
# Solution Started: Nov 26, 2024
# Puzzle Link: https://adventofcode.com/2021/day/23
# Solution by: [abbasmoosajee07]
# Brief: [Sliding Puzzles]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from heapq import heappop, heappush

# Load the input data from the specified file path
D23_file = "Day23_input.txt"
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

# Read and sort input data into a grid
with open(D23_file_path) as file:
    floors_init = file.read().strip().split('\n')

def can_leave_room(puzzle, room_positions, room_type):
    """
    Determines if an amphipod can leave its designated room.
    - Returns the position of the amphipod if it can leave.
    - Returns False if all amphipods in the room are correctly placed.
    """
    # Check if all occupied positions match the target room type.
    if all(puzzle[pos] == room_type for pos in room_positions if puzzle[pos] != '.'):
        return False

    # Find the first amphipod that can move.
    for pos in room_positions:
        if puzzle[pos] != '.':
            return pos

def blocked(start, end, puzzle):
    """
    Checks if the path between `start` and `end` is blocked by other amphipods.
    """
    step = 1 if start < end else -1
    for pos in range(start + step, end + step, step):
        if puzzle[pos] != '.':
            return True
    return False

def get_possible_parking_positions(start, parking_positions, puzzle):
    """
    Yields possible parking positions that the amphipod at `start` can move to.
    """
    for pos in parking_positions:
        if puzzle[pos] == '.' and not blocked(start, pos, puzzle):
            yield pos

def move_amphipod(start, end, puzzle):
    """
    Moves an amphipod from `start` to `end` in the puzzle state.
    Returns the new puzzle state.
    """
    puzzle_list = list(puzzle)
    puzzle_list[start], puzzle_list[end] = puzzle_list[end], puzzle_list[start]
    return ''.join(puzzle_list)

def can_enter_room(start, room_entry, amphipod_type, puzzle, room_positions):
    """
    Checks if an amphipod can enter its target room.
    - Returns the best available position in the room if possible.
    - Returns False if the room is not accessible or contains incorrect amphipods.
    """
    best_position = None

    for pos in room_positions:
        if puzzle[pos] == '.':
            best_position = pos  # Update to the deepest available position.
        elif puzzle[pos] != amphipod_type:
            return False  # Room contains an incorrect amphipod.

    # Ensure the path to the room is not blocked.
    if not blocked(start, room_entry, puzzle):
        return best_position

def possible_moves(puzzle, parking_positions, room_entries, room_targets):
    """
    Yields all possible valid moves (start, end) for the current puzzle state.
    """
    # Check if any amphipod in the parking area can enter its target room.
    for start in parking_positions:
        if puzzle[start] != '.':
            amphipod_type = puzzle[start]
            if (end := can_enter_room(start, room_entries[amphipod_type], amphipod_type, puzzle, room_targets[amphipod_type])):
                yield start, end

    # Check if any amphipod can leave its room.
    for room_type in 'ABCD':
        if (start := can_leave_room(puzzle, room_targets[room_type], room_type)):
            for end in get_possible_parking_positions(room_entries[room_type], parking_positions, puzzle):
                yield start, end

def solve(puzzle):
    """
    Solves the amphipod puzzle using a priority queue (Dijkstra's algorithm).
    """
    # Energy cost per amphipod type.
    energy_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

    # Define parking positions and room entry points.
    parking_positions = [0, 1, 3, 5, 7, 9, 10]
    room_entries = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
    room_targets = {room: range(ord(room) - 54, len(puzzle), 4) for room in 'ABCD'}
    targetI = {pos: room for room, positions in room_targets.items() for pos in positions}  # Reverse lookup for room type.

    # Define the target state (all amphipods in their rooms).
    target_state = '.' * 11 + 'ABCD' * ((len(puzzle) - 11) // 4)

    # Priority queue and visited states for Dijkstra's algorithm.
    heap = [(0, puzzle)]
    seen_states = {puzzle: 0}

    while heap:
        current_cost, current_state = heappop(heap)

        # Return the cost if the target state is reached.
        if current_state == target_state:
            return current_cost

        # Explore possible moves.
        for start, end in possible_moves(current_state, parking_positions, room_entries, room_targets):
            # Calculate move distance and energy cost.
            parking, room_pos = (start, end) if start < end else (end, start)
            room_type = targetI[room_pos]  # Determine the room type using the reverse lookup dictionary.
            distance = abs(room_entries[room_type] - parking) + (room_pos - 7) // 4
            new_cost = current_cost + distance * energy_cost[current_state[start]]

            # Generate the new state.
            new_state = move_amphipod(start, end, current_state)

            # Skip if this state has already been visited with a lower cost.
            if new_cost >= seen_states.get(new_state, float('inf')):
                continue

            # Update the state and add it to the priority queue.
            seen_states[new_state] = new_cost
            heappush(heap, (new_cost, new_state))


# Example usage: Provide the file path containing the puzzle input.
room_p1 = ''.join(letter for row in floors_init
                    for letter in row if letter in 'ABCD.')
energy_p1 = solve(room_p1)
print("Part 1:", energy_p1)

extra_floors =["#D#C#B#A#", "#D#B#A#C#"]
# Combine input_data with additional_lines at the desired position using slicing
floors_p2 = (
    floors_init[:3]        # First three floors
    + extra_floors         # Add additional floors
    + floors_init[3:]      # Remaining floors
)
room_p2 = ''.join(letter for row in floors_p2
                    for letter in row if letter in 'ABCD.')
energy_p2 = solve(room_p2)
print("Part 2:", energy_p2)