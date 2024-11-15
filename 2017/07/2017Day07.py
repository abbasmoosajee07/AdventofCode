# Advent of Code - Day 7, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/7
# Solution by: [abbasmoosajee07]
# Brief: [Creating Weighted Word Trees]

import os, re
import numpy as np
import collections

# Load the input file
D7_file = 'Day07_input.txt'
D7_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D7_file)

# Load input data from the specified file path
with open(D7_file_path) as file:
    input_data = file.read().splitlines()

# print(input_data)

words = []
bad_words = set()

# Process each line of input data to build words and bad words set
for line in input_data:
    # Split the line into parts and strip whitespace
    parts = line.strip().split()
    words.append(parts[0])  # Always add the first part to the words list
    
    # Check if there's a "->" indicating a bad word relationship
    if "->" in line:
        index = parts.index("->")
        # Extract bad words from the line after "->" and clean up
        bad_children = [child.strip(",") for child in parts[index + 1:]]
        bad_words.update(bad_children)  # Add bad words to the set

# Print words that are not in the bad words set
for word in words:
    if word not in bad_words:
        print(f"Part 1: Word at the bottom of the tree: {word}")

# Initialize weight and children dictionaries
weight = {}
children = {}

# Process the input data for weights and children relationships
for line in input_data:
    match = re.match(r'(\w+) \((\d+)\)(?: -> (.+))?', line)
    if match:
        label = match.group(1)
        n = int(match.group(2))
        weight[label] = n  # Store the weight
        if match.group(3):
            # Split the children if present
            children[label] = tuple(child.strip() for child in match.group(3).split(','))
        else:
            children[label] = ()

# Find the root (the node without a parent)
all_children = {c for cs in children.values() for c in cs}
root = next(label for label in weight if label not in all_children)

def total_weight(label):
    # Calculate total weight recursively
    sub_weights = [total_weight(c) for c in children[label]]
    if len(set(sub_weights)) > 1:
        # Find the weights that do not match
        (target, _), (failure, _) = collections.Counter(sub_weights).most_common()
        # Adjust the output for the unbalanced node
        unbalanced_index = sub_weights.index(failure)
        print(f"Correct weight for unbalanced child '{children[label][unbalanced_index]}': {target - failure + weight[children[label][unbalanced_index]]}")
    return weight[label] + sum(sub_weights)

# Calculate the total weight starting from the root
print(f"Total weight of '{root}': {total_weight(root)}")
