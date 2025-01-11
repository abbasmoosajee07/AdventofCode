"""Advent of Code - Day 21, Year 2023
Solution Started: Jan 11, 2025
Puzzle Link: https://adventofcode.com/2023/day/21
Solution by: abbasmoosajee07
Brief: [Help Lost Gardener]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
start_time = time.time()

# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_grid(init_grid: list) -> tuple[set, tuple]:
    rocks = set()

    # Initialize boundaries with extreme values
    min_row, max_row = float('inf'), -float('inf')
    min_col, max_col = float('inf'), -float('inf')

    # Iterate through the grid to update each tile to dict and update bounds
    for row_no, row in enumerate(init_grid):
        for col_no, tile in enumerate(row):
            if tile == '#':
                rocks.add((row_no, col_no))
            elif tile == 'S':
                start = (row_no, col_no)

            # Update the boundaries
            min_row = min(min_row, row_no)
            max_row = max(max_row, row_no)
            min_col = min(min_col, col_no)
            max_col = max(max_col, col_no)

    # Define the space bounds
    grid_bounds = (min_row, max_row + 1, min_col, max_col + 1)

    return rocks, grid_bounds, start

def print_grid(ROCKS: set, grid_bounds: tuple, movements: dict):
    min_row, max_row, min_col, max_col = grid_bounds
    grid_list = []

    for row_no in range(min_row, max_row):
        row = ''
        for col_no in range(min_col, max_col):
            pos = (row_no, col_no)

            if pos in ROCKS:
                row += ' # '
            elif pos in movements.keys():
                row += str(movements[pos]).zfill(3)

            else:
                row += ' . '

        grid_list.append(row)

    # Print grid
    print("\nCurrent Grid:")
    for row in grid_list:
        print("".join(row))
    print()

def build_graph(ROCKS_SET: set[tuple], BOUNDARIES: tuple):
    def get_neighbors(init_pos: tuple) -> set:
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = set()
        init_row, init_col = init_pos
        for dr, dc in DIRECTIONS:
            next_row, next_col = init_row + dr, init_col + dc
            if (
                MIN_ROW <= next_row < MAX_ROW and
                MIN_COL <= next_col < MAX_COL and
                (next_row, next_col) not in ROCKS_SET
            ):
                neighbors.add((next_row, next_col))
        return neighbors
    graph_network = {}
    MIN_ROW, MAX_ROW, MIN_COL, MAX_COL = BOUNDARIES
    for row in range(MIN_ROW, MAX_ROW):
        for col in range(MIN_COL, MAX_COL):
            pos = (row, col)
            neighbors = get_neighbors(pos)
            graph_network[pos] = neighbors
    return graph_network

def traverse_garden(garden_graph: dict, start: tuple, target_steps: int = 64) -> dict:
    visited = set()
    queue = deque([(start, 0)])  # Use deque for efficient queue operations
    possible_plants = {start: 'S'}
    while queue:
        current_pos, steps = queue.popleft()
        if steps == target_steps:
            break
        steps += 1
        visited.add(current_pos)
        # Get the valid neighboring positions (plants) from the garden graph
        neighbor_plants = garden_graph.get(current_pos, [])

        for plant_pos in neighbor_plants:
            if plant_pos not in visited:
                visited.add(plant_pos)
                queue.append((plant_pos, steps))
                # Increment total for every even step
                if steps % 2 == 0:
                    possible_plants[plant_pos] = steps
    return possible_plants

def traverse_infinite_garden(garden_graph: dict, start: tuple, boundaries: tuple) -> int:
    """ Traverse an infinite garden represented as a graph and calculate reachable plant tiles. """

    visited = {}  # Keeps track of visited points and their distances
    grid_size = boundaries[1]  # Maximum boundary size
    queue = deque([(start, 0)])  # (current point, distance from start)

    def count_plants(condition):
        """Helper function to count points in visited where a condition is true."""
        return sum(1 for v in visited.values() if condition(v))

    # Perform BFS traversal to visit all reachable points
    while queue:
        point, distance = queue.popleft()

        if point in visited:
            continue

        visited[point] = distance

        for neighbor in garden_graph.get(point, []):
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))

    # Calculate distance to edge and validate assumptions
    distance_to_edge = grid_size // 2
    assert distance_to_edge == 65, f"Unexpected distance to edge, got {distance_to_edge}"

    n = (26501365 - distance_to_edge) // grid_size
    assert n == 202300, f"n calculation is incorrect, got {n}"

    # Calculate the number of odd and even tiles
    num_odd_tiles = (n + 1) ** 2
    num_even_tiles = n ** 2

    # Count odd and even corners beyond the edge
    odd_corners = count_plants(lambda v: v > distance_to_edge and v % 2 == 1)
    even_corners = count_plants(lambda v: v > distance_to_edge and v % 2 == 0)

    # Calculate all reachable plant tiles
    all_reachable_plants = (
        num_odd_tiles * count_plants(lambda v: v % 2 == 1)
        + num_even_tiles * count_plants(lambda v: v % 2 == 0)
        - ((n + 1) * odd_corners)
        + (n * even_corners)
    )

    return all_reachable_plants

test_input = ['...........', '.....###.#.', '.###.##..#.', '..#.#...#..', '....#.#....', '.##..S####.', '.##..#...#.', '.......##..', '.##.#.####.', '.##..##.##.', '...........']

ROCKS_SET, BOUNDARIES, start_pos = parse_grid(input_data)
garden_graph = build_graph(ROCKS_SET, BOUNDARIES)
plants_reached = traverse_garden(garden_graph, start_pos, 64)
print("Part 1:", len(plants_reached))

infinte_garden = traverse_infinite_garden(garden_graph,start_pos, BOUNDARIES)
print("Part 2:", infinte_garden)

# print(f"Execution Time = {time.time() - start_time:.5f}")
