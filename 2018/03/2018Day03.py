# Advent of Code - Day 3, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/3
# Solution by: [abbasmoosajee07]
# Brief: [Fabric grids and claims]

import os, re
import pandas as pd
import numpy as np
from collections import Counter

# Load the input data from the specified file path
D3_file = "Day03_input.txt"
D3_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D3_file)

with open(D3_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_claims(claims_list):
    # List to store parsed commands
    claim_properties = []

    # Regular expression for each claim pair command
    claim_pattern = r"#(\d+)\s+@\s+(\d+),(\d+):\s+(\d+)x(\d+)"

    for claim_pair in claims_list:
        claim_match = re.match(claim_pattern, claim_pair)
        if claim_match:
            ID, left, top, wide, tall = map(int, claim_match.groups())
            claim_properties.append([ID, left, top, wide, tall, wide*tall])

    return pd.DataFrame(claim_properties, columns=['ID', 'left', 'top', 'wide', 'tall', 'total'])

def claim_fabric(matrix, claim):
    top, left, tall, wide = claim['top'], claim['left'], claim['tall'], claim['wide']

    for row in range(top, top + tall):
        for col in range(left, left + wide):
            # Append the claim ID to the list at this cell
            matrix[row, col].append(claim['ID'])
    return matrix

def map_fabric_claims(claim_df, size = 1000):
    # Initialize a 1000x1000 fabric matrix with empty lists in each cell
    fabric_matrix = np.empty((size, size), dtype=object)
    for i in range(fabric_matrix.shape[0]):
        for j in range(fabric_matrix.shape[1]):
            fabric_matrix[i, j] = []  # Initialize each cell as an empty list

    # Apply claims to the fabric
    current_matrix = fabric_matrix
    for claim_n in range(len(claim_df)):
        current_matrix = claim_fabric(current_matrix, claim_df.loc[claim_n])

    return current_matrix

# Parse claims
claim_df = parse_claims(input_data)
claimed_fabric = map_fabric_claims(claim_df)

# # Print a section of the matrix to verify (optional)
# for row in current_matrix:
#     print([cell for cell in row])

# Initialize variables
multiple_claims = 0
unique_claims = []
overlapping_claims = set()  # Set to store IDs of overlapping claims

# Iterate through the claimed fabric
for row in range(len(claimed_fabric)):
    for col in range(len(claimed_fabric[row])):
        # Check if there are multiple claims on this cell
        if len(claimed_fabric[row, col]) >= 2:
            multiple_claims += 1
            overlapping_claims.update(claimed_fabric[row, col])  # Add overlapping IDs to the set
        elif len(claimed_fabric[row, col]) == 1:
            num = claimed_fabric[row, col][0]  # Access the first (and only) ID
            unique_claims.append(num)

# Now filter unique claims to exclude those in overlapping_claims
unique_claims = [claim for claim in unique_claims if claim not in overlapping_claims]

# Print results
print(f"Part 1: Total overlapping cells: {multiple_claims}")
print(f"Part 2: Unique Claim ID {unique_claims[0]} for a length of {len(unique_claims)}")

