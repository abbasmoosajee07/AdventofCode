"""Advent of Code - Day 22, Year 2023
Solution Started: Jan 11, 2025
Puzzle Link: https://adventofcode.com/2023/day/22
Solution by: abbasmoosajee07
Brief: [Tower of Bricks]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Read and sort input data into a grid
with open(D22_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_list: list[str]) -> dict:
    graph = {}
    for brick_no, line in enumerate(input_list, start=1):
        # Parse the coordinates from the input string
        edge_1, edge_2 = line.split('~')
        edge_1_coords = tuple(map(int, edge_1.split(',')))
        edge_2_coords = tuple(map(int, edge_2.split(',')))
        # Store the brick name and the coordinates in the graph
        # print(brick_no, brick_name, edge_1_coords, edge_2_coords)
        graph[brick_no] = (edge_1_coords, edge_2_coords)
    return graph

def build_tower(brick_graph: dict):
    blocks = list(brick_graph.values())
    blocks.sort(key=lambda x: x[1][2]) # sort by z1: distance to ground
    X_MAX = max(b[1][0] for b in blocks) + 1
    Y_MAX = max(b[1][1] for b in blocks) + 1
    Z_MAX = max(b[1][2] for b in blocks) + 1
    BLOCKS_NO = len(blocks)

    stack = [[['empty' for _ in range(X_MAX)]
                for _ in range(Y_MAX)]
                for _ in range(Z_MAX)]

    supported_by = {}

    for block_id, ((x1, y1, z1), (x2, y2, z2)) in enumerate(blocks):
        # Determine the height of the block
        height = z2 - z1 + 1

        # Let the block fall until it receives support
        for z in range(Z_MAX):
            # Collect support for the block at this level
            support = {
                stack[z][y][x]
                for x in range(x1, x2 + 1)
                for y in range(y1, y2 + 1)
            } - {'empty'}

            # If there is support, record it and stop falling
            if support:
                supported_by[block_id] = support
                break

        # Add the block above its support
        for z_ in range(z - height, z):
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    stack[z_][y][x] = block_id

    # Disintegrate indispensible blocks & examine the resulting chain reactions
    indispensible = set.union(*[x for x in supported_by.values() if len(x)==1])
    total = 0
    for i in indispensible:
        disintegrated = set([i])
        for j in range(i+1, BLOCKS_NO):
            if j in supported_by and supported_by[j].issubset(disintegrated):
                disintegrated.add(j)
        total += len(disintegrated) - 1

    return len(blocks) - len(indispensible), total

brick_graph = parse_input(input_data)

ans_p1, ans_p2 = build_tower(brick_graph)
print("Part 1:", ans_p1)
print("Part 2:", ans_p2)

# print(f"Execution Time = {time.time() - start_time:.5f}")
