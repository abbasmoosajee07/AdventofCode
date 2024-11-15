# Advent of Code - Day 20, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/20
# Solution by: [abbasmoosajee07]
# Brief: [Building a maze and solving it]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    input_data = file.read().strip().split('\n')[0]

def build_maze(regex):
    graph = nx.Graph()
    directions = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}
    start = (0, 0)
    stack = []

    graph.add_node(start)
    current_position = start

    for char in regex:
        if char in 'NSEW':
            dx, dy = directions[char]
            next_position = (current_position[0] + dx, current_position[1] + dy)
            graph.add_edge(current_position, next_position)
            current_position = next_position
        elif char == '(':
            stack.append(current_position)
        elif char == ')':
            current_position = stack.pop()
        elif char == '|':
            current_position = stack[-1]

    return graph, start


graph, start = build_maze(input_data)

# Calculate shortest paths from the starting position
lengths = nx.shortest_path_length(graph, source=start)

# Part 1: Maximum distance to any room
max_distance_p1 = max(lengths.values())
print(f"Part 1: {max_distance_p1}")


# Part 2: Count rooms at least 1000 doors away
doors_1000_p2 = sum(1 for distance in lengths.values() if distance >= 1000)
print(f"Part 2: {doors_1000_p2}")