# Advent of Code - Day 22, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Navigating Caves, P2]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import networkx as nx

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

import networkx as nx

# Terrain types
ROCKY, WET, NARROW = 0, 1, 2

# Equipment types
TORCH, CLIMBING_GEAR, NEITHER = 0, 1, 2

# Valid equipment for each terrain type
VALID_EQUIPMENT = {
    ROCKY: (TORCH, CLIMBING_GEAR),
    WET: (CLIMBING_GEAR, NEITHER),
    NARROW: (TORCH, NEITHER)
}

# Valid terrains for each equipment type
VALID_TERRAINS = {
    TORCH: (ROCKY, NARROW),
    CLIMBING_GEAR: (ROCKY, WET),
    NEITHER: (WET, NARROW)
}


def parse_input(file_path):
    with open(file_path) as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]
        depth = int(lines[0][len("depth: "):])
        target = tuple(map(int, lines[1][len("target: "):].split(",")))
    return depth, target


def generate_cave_grid(depth, max_corner, target):
    # Grid mapping (x, y) -> (geologic index, erosion level, risk level)
    cave_grid = {}

    for y in range(0, max_corner[1] + 1):
        for x in range(0, max_corner[0] + 1):
            if (x, y) in [(0, 0), target]:
                geo_index = 0
            elif x == 0:
                geo_index = y * 48271
            elif y == 0:
                geo_index = x * 16807
            else:
                geo_index = cave_grid[(x-1, y)][1] * cave_grid[(x, y-1)][1]
            erosion_level = (geo_index + depth) % 20183
            risk_level = erosion_level % 3
            cave_grid[(x, y)] = (geo_index, erosion_level, risk_level)

    return cave_grid


def find_shortest_path(cave_grid, max_corner, target):
    graph = nx.Graph()
    for y in range(0, max_corner[1] + 1):
        for x in range(0, max_corner[0] + 1):
            terrain = cave_grid[(x, y)][2]
            equipment = VALID_EQUIPMENT[terrain]
            # Add edges for switching equipment
            graph.add_edge((x, y, equipment[0]), (x, y, equipment[1]), weight=7)
            # Add edges for moving between neighboring cells
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                n_x, n_y = x + dx, y + dy
                if 0 <= n_x <= max_corner[0] and 0 <= n_y <= max_corner[1]:
                    neighbor_terrain = cave_grid[(n_x, n_y)][2]
                    neighbor_equipment = VALID_EQUIPMENT[neighbor_terrain]
                    for item in set(equipment).intersection(set(neighbor_equipment)):
                        graph.add_edge((x, y, item), (n_x, n_y, item), weight=1)

    return nx.dijkstra_path_length(graph, (0, 0, TORCH), (target[0], target[1], TORCH))

# Parse input
depth, target = parse_input(D22_file_path)

# Define the cave grid dimensions
max_corner = (target[0] + 100, target[1] + 100)

# Generate the cave grid
cave_grid = generate_cave_grid(depth, max_corner, target)

# Find the shortest path
print("Part 2:", find_shortest_path(cave_grid, max_corner, target))
