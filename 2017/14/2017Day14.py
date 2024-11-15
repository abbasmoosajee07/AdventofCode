# Advent of Code - Day 14, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/14
# Solution by: [abbasmoosajee07]
# Brief: [Building Hash grids]


import os, re, copy, hashlib
import numpy as np

# Load the input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

with open(D14_file_path) as file:
    input = file.read()

def build_hash(num_list, length, skip_size, current_position):
    """Single round of the Knot Hash algorithm."""
    list_len = len(num_list)
    
    # Extract sublist with circular wrapping and reverse it
    sub_list = [num_list[(current_position + i) % list_len] for i in range(length)]
    sub_list.reverse()
    
    # Replace the original elements in the circular list
    for i in range(length):
        num_list[(current_position + i) % list_len] = sub_list[i]
    
    # Update position and skip size
    current_position = (current_position + length + skip_size) % list_len
    skip_size += 1
    
    return num_list, current_position, skip_size

def knot_hash(input_string):
    """Computes the Knot Hash for a given input string."""
    # Step 1: Convert input string to ASCII codes and append the suffix
    ascii_lengths = [ord(c) for c in input_string] + [17, 31, 73, 47, 23]
    
    # Step 2: Initialize the list, position, and skip size
    num_list = list(range(256))
    current_position = 0
    skip_size = 0

    # Step 3: Perform 64 rounds
    for _ in range(64):
        for length in ascii_lengths:
            num_list, current_position, skip_size = build_hash(num_list, length, skip_size, current_position)

    # Step 4: Create the dense hash by XOR-ing blocks of 16 numbers
    dense_hash = []
    for block_start in range(0, 256, 16):
        xor_result = 0
        for i in range(16):
            xor_result ^= num_list[block_start + i]
        dense_hash.append(xor_result)

    # Step 5: Convert dense hash to hexadecimal format
    hex_hash = ''.join(f'{num:02x}' for num in dense_hash)
    # print(dense_hash)
    return hex_hash



def hex_to_4bit_binary(hex_string):
    # Remove any whitespace and convert to upper case for uniformity
    hex_string = hex_string.replace(" ", "").upper()
    
    # Ensure we have exactly 32 hex digits
    if len(hex_string) != 32:
        raise ValueError("Input must contain exactly 32 hexadecimal digits.")

    # Convert each hexadecimal digit to a 4-bit binary representation
    binary_values = [f"{int(char, 16):04b}" for char in hex_string]

    # Join the binary values into a single string or return as a list
    binary_string = ''.join(binary_values)
    
    return binary_string


def count_regions(grid):
    rows, cols = len(grid), len(grid[0])  # Dimensions of the grid
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    def dfs(x, y):
        # Base case: check for boundaries and if already visited or is '0'
        if x < 0 or y < 0 or x >= rows or y >= cols or visited[x][y] or grid[x][y] == '0':
            return
        visited[x][y] = True  # Mark the cell as visited
        # Explore all 4 adjacent directions (up, down, left, right)
        dfs(x + 1, y)  # Down
        dfs(x - 1, y)  # Up
        dfs(x, y + 1)  # Right
        dfs(x, y - 1)  # Left

    region_count = 0
    for i in range(rows):
        for j in range(cols):
            # If we find an unvisited '1', it's a new region
            if grid[i][j] == '1' and not visited[i][j]:
                dfs(i, j)  # Perform DFS to mark all cells in this region
                region_count += 1  # Increment the region count

    return region_count

def create_hash_grid(string):
    hash_grid = []
    sum = 0
    for row in range(0,128,1):
        row_input = f"{string}-{str(row)}"
        row_hash = knot_hash(str(row_input))
        row_binary = hex_to_4bit_binary(row_hash)
        hash_grid.append(row_binary)
        sum_1 = row_binary.count('1')
        sum += sum_1
    
    return hash_grid, sum

"""------------------------- Example usage ------------------------"""

hash_grid, sum = create_hash_grid(input)
print(f"Part 1: sum of 1s is {sum}")

# Convert each row string to a list of characters for easy handling
hash_grid = [list(row) for row in hash_grid]
regions = count_regions(hash_grid)
print(f"Part 2: Number of regions: {regions}")
