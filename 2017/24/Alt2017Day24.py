# Advent of Code - Day 24, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/24
# Solution by: [abbasmoosajee07]
# Brief: [Building Bridges V_Python]

import os, copy
from collections import Counter

# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_list = [list(map(int, line.split('/'))) for line in input_data]

def find_bridges(components, bridge=[], port=0):
    """Recursively finds all bridges that can be created."""
    possible_bridges = [bridge]

    # Explore each component that has a matching port
    for component in components:
        if port in component:
            # Choose the component, orient it correctly
            next_port = component[1] if component[0] == port else component[0]
            new_components = components[:]
            new_components.remove(component)
            possible_bridges += find_bridges(new_components, bridge + [component], next_port)

    return possible_bridges

# Generate all possible bridges starting with port 0
all_bridges = find_bridges(input_list)

# Calculate the strengths of all possible bridges
bridge_strengths = [sum(sum(pair) for pair in bridge) for bridge in all_bridges]
longest_bridge = max(all_bridges, key=lambda b: (len(b), sum(sum(pair) for pair in b)))

# # Output all results
# print("All possible bridges and their strengths:")
# for bridge, strength in zip(all_bridges, bridge_strengths):
#     print(f"Bridge: {bridge}, Strength: {strength}")

# Part 1: Find the strongest bridge
strongest_bridge = max(bridge_strengths)
print(f"Strongest bridge strength: {strongest_bridge}")

# Part 2: Find the longest bridge (if multiple, choose the strongest of them)
longest_strength = sum(sum(pair) for pair in longest_bridge)
print(f"Longest bridge: {longest_bridge}, Strength: {longest_strength}")
