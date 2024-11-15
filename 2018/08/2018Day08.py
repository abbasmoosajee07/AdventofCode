# Advent of Code - Day 8, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/8
# Solution by: [abbasmoosajee07]
# Brief: [Nodes and Children]

import os, re
import numpy as np
import pandas as pd

# Load the input data from the specified file path
D8_file = "Day08_input.txt"
D8_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D8_file)

# Read and sort input data into a grid
with open(D8_file_path) as file:
    input_data = file.read().strip().split()
    input_data = [int(x) for x in input_data]

# print(input_data)
num_list = input_data

def parse_node(data, index):
    # Read header
    num_children = data[index]
    num_metadata = data[index + 1]
    index += 2
    
    # Part 1: Sum of all metadata entries
    metadata_sum = 0
    child_values = []
    
    # Parse child nodes and gather their values
    for _ in range(num_children):
        child_value, child_metadata_sum, index = parse_node(data, index)
        metadata_sum += child_metadata_sum  # Accumulate metadata from children
        child_values.append(child_value)  # Store child node values for Part 2
    
    # Parse metadata entries
    metadata = data[index:index + num_metadata]
    metadata_sum += sum(metadata)  # Part 1: Add metadata entries to total sum
    index += num_metadata
    
    # Part 2: Node value calculation
    if num_children == 0:
        # If no children, node value is the sum of its metadata
        node_value = sum(metadata)
    else:
        # If there are children, metadata entries act as indices to child values
        node_value = sum(child_values[i - 1] for i in metadata if 1 <= i <= len(child_values))
    
    return node_value, metadata_sum, index

# Usage
root_value, metadata_sum, _ = parse_node(input_data, 0)
print("Part 1 - Metadata Sum:", metadata_sum)
print("Part 2 - Root Node Value:", root_value)
