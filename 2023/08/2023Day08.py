"""Advent of Code - Day 8, Year 2023
Solution Started: Dec 25, 2024
Puzzle Link: https://adventofcode.com/2023/day/8
Solution by: abbasmoosajee07
Brief: [Traversing Node Networks]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import gcd

# Load the input data from the specified file path
D08_file = "Day08_input.txt"
D08_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D08_file)

# Read and sort input data into a grid
with open(D08_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_input(input_list: list[str]) -> tuple[list, dict]:
    binary_movements = input_list[0].replace('L', '0').replace('R', '1')
    movements = list(map(int, binary_movements))
    nodes_dict = {}
    for line in input_list[1].split('\n'):
        main_node, next_nodes = line.split(' = ')
        parsed_str = next_nodes.replace('(','').replace(')','')
        nodes_dict[main_node] = tuple(parsed_str.split(', '))
    return movements, nodes_dict

def lcm(values):
    """Calculate the least common multiple of a list of integers."""
    result = 1
    for value in values:
        result = (value * result) // gcd(value, result)
    return result


def move_in_network(movements: list[int], node_transitions: dict, ghosts: bool=False) -> int:
    # Initialize positions based on presence of ghosts
    initial_nodes = [node for node in node_transitions if node.endswith('A' if ghosts else 'AAA')]
    current_positions = initial_nodes

    # Dictionary to track when nodes reach target states
    target_times = {}
    steps = 0

    while True:
        new_positions = []
        for index, position in enumerate(current_positions):
            # Determine the next position for the current node
            next_position = node_transitions[position][movements[steps % len(movements)]]
            if next_position.endswith('Z'):
                # Record the step when a node reaches a target state
                target_times[index] = steps + 1
                if len(target_times) == len(initial_nodes):
                    # All nodes have reached the target state; calculate the result
                    return lcm(target_times.values())
            new_positions.append(next_position)

        current_positions = new_positions
        steps += 1

movements, node_transitions = parse_input(input_data)

steps_p1 = move_in_network(movements, node_transitions)
print("Part 1:", steps_p1)

steps_p2 = move_in_network(movements, node_transitions, ghosts=True)
print("Part 2:", steps_p2)
