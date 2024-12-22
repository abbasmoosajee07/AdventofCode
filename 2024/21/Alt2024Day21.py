"""Advent of Code - Day 21, Year 2024
Solution Started: Dec 21, 2024
Puzzle Link: https://adventofcode.com/2024/day/21
Solution by: abbasmoosajee07
Brief: [Using robots for keypads]
"""

#!/usr/bin/env python3

import os, re, copy,time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from typing import List, Dict, Tuple

start_time = time.time()
# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split('\n')

def sanitize_paths(paths: List[str], start_pos: Tuple[int, int], is_numeric: bool) -> List[str]:
    """Sanitizes paths by removing those that pass through excluded positions."""
    excluded_position = NUMERIC_POS['X'] if is_numeric else DIRECTIONAL_POS['X']
    DIRECTIONAL_KEYS: Dict[str, Tuple[int, int]] = {'^': (-1, 0), 'v': (1, 0), '>': (0, 1), '<': (0, -1)}  # Up, Down, Right, Left
    i = 0
    while i < len(paths):
        current_pos = list(start_pos)
        for direction in paths[i]:
            dr, dc = DIRECTIONAL_KEYS[direction]
            current_pos[0] += dr
            current_pos[1] += dc

            if tuple(current_pos) == excluded_position:
                paths.pop(i)
                i -= 1
                break
        i += 1

    return paths

def get_shortest_paths(start_pos: Tuple[int, int], end_pos: Tuple[int, int], is_numeric: bool) -> List[str]:
    """Generates shortest paths between start and end positions."""
    vertical_move = "^" if end_pos[0] - start_pos[0] < 0 else "v"
    vertical_distance = abs(end_pos[0] - start_pos[0])
    horizontal_move = "<" if end_pos[1] - start_pos[1] < 0 else ">"
    horizontal_distance = abs(end_pos[1] - start_pos[1])

    raw_paths = [
        vertical_move * vertical_distance + horizontal_move * horizontal_distance,
        horizontal_move * horizontal_distance + vertical_move * vertical_distance
    ]

    return sanitize_paths(list(set(raw_paths)), start_pos, is_numeric)

def solve_numeric_keypad(number_sequence: str) -> List[List[str]]:
    """Generates sequences to navigate a numeric keypad."""
    current_pos: Tuple[int, int] = NUMERIC_POS["A"]
    sequence: List[List[str]] = []

    for digit in number_sequence:
        target_pos = NUMERIC_POS[digit]
        paths = get_shortest_paths(current_pos, target_pos, is_numeric=True)
        current_pos = target_pos
        sequence.append(paths)

    sequence_parts: List[List[str]] = []
    for part in sequence:
        sequence_parts.append(["".join(path) + "A" for path in part])

    return sequence_parts

def solve_directional_keypad(direction_sequence: str) -> List[List[str]]:
    """Generates sequences to navigate a directional keypad."""
    current_pos: Tuple[int, int] = DIRECTIONAL_POS["A"]
    sequence: List[List[str]] = []

    for direction in direction_sequence:
        target_pos = DIRECTIONAL_POS[direction]
        paths = get_shortest_paths(current_pos, target_pos, is_numeric=False)
        current_pos = target_pos
        sequence.append(paths)

    sequence_parts: List[List[str]] = []
    for part in sequence:
        sequence_parts.append(["".join(path) + "A" for path in part])

    return sequence_parts

def calculate_min_cost(sequence: str, depth: int) -> int:
    """Calculates the minimum cost to type a sequence with a given depth."""
    if depth == 0:
        return len(sequence)

    if (sequence, depth) in memory:
        return memory[(sequence, depth)]

    sub_sequences = solve_directional_keypad(sequence)
    cost = sum(
        min([calculate_min_cost(sub_seq, depth - 1) for sub_seq in part]) for part in sub_sequences
    )

    memory[(sequence, depth)] = cost
    return cost

def calculate_complexity(keycodes: List[str], depth: int) -> int:
    """Solves the puzzle for a given depth level."""
    total_cost = 0
    for key in keycodes:
        numeric_sequence = solve_numeric_keypad(key)
        level_cost = sum(
            min(calculate_min_cost(sequence, depth) for sequence in part)
            for part in numeric_sequence
        )
        total_cost += int(key[:-1]) * level_cost

    return total_cost

def parse_keypads(keypad: List[List[str]]) -> Dict[str, Tuple[int, int]]:
    """Parses a keypad layout into a dictionary of positions."""
    positions = {}
    for r, row in enumerate(keypad):
        for c, key in enumerate(row):
            positions[key] = (r, c)
    return positions

# Global variables
global memory, NUMERICAL_KEYPAD, DIRECTION_KEYPAD, NUMERIC_POS, DIRECTIONAL_POS
memory: Dict[Tuple[str, int], int] = {}
NUMERICAL_KEYPAD: List[List[str]] = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['X', '0', 'A']
]

DIRECTION_KEYPAD: List[List[str]] = [
    ['X', '^', 'A'],
    ['<', 'v', '>']
]

NUMERIC_POS: Dict[str, Tuple[int, int]] = parse_keypads(NUMERICAL_KEYPAD)
DIRECTIONAL_POS: Dict[str, Tuple[int, int]] = parse_keypads(DIRECTION_KEYPAD)

# Example usage
complex_cost_p1: int = calculate_complexity(input_data, 2)
print("Part 1:", complex_cost_p1)

complex_cost_p2: int = calculate_complexity(input_data, 25)
print("Part 2:", complex_cost_p2)
print(time.time()-start_time)