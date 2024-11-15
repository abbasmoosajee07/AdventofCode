# Advent of Code - Day 21, Year 2117
# Solved in 2124
# Puzzle Link: https://adventofcode.com/2017/day/21
# Solution by: [abbasmoosajee07]
# Brief: [Particle Racing]

import os, re, copy
import pandas as pd
import numpy as np

# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

with open(D21_file_path) as file:
    input_data = file.readlines()

import numpy as np

# Dictionary to store the transformation mappings
transformations = {}

# Starting pattern for the grid
initial_grid_pattern = '.#./..#/###'


def convert_to_numpy(pattern):
    """
    Converts a pattern string into a NumPy array where '#' is True and '.' is False.
    """
    return np.array([[cell == '#' for cell in row] for row in pattern.split('/')])


# Parse the input data to build the transformation mappings
for line in input_data:
    # Separate the pattern (key) and its transformation (value)
    pattern, result = map(convert_to_numpy, line.strip().split(' => '))
    
    # Generate all 4 rotations and both flipped versions of the pattern
    for flipped_pattern in (pattern, np.fliplr(pattern)):
        for rotation in range(4):
            rotated_pattern = np.rot90(flipped_pattern, rotation)
            transformations[rotated_pattern.tobytes()] = result


def enhance_grid(grid):
    """
    Enhances the grid by dividing it into 2x2 or 3x3 blocks, transforming each block if a transformation exists,
    and stitching the transformed (or unchanged) blocks back together into a new grid.
    """
    grid_size = len(grid)
    block_size = 2 if grid_size % 2 == 0 else 3  # Use 2x2 or 3x3 blocks depending on grid size
    new_block_size = block_size + 1  # Transformed blocks are one size larger
    new_grid_size = (grid_size * new_block_size) // block_size  # Calculate the size of the enhanced grid
    enhanced_grid = np.empty((new_grid_size, new_grid_size), dtype=bool)  # Initialize the enhanced grid

    # Define ranges for iterating over blocks in the original and enhanced grids
    original_grid_blocks = range(0, grid_size, block_size)
    enhanced_grid_blocks = range(0, new_grid_size, new_block_size)

    # Iterate through each block in the grid, apply the transformation if it exists, and place it in the new grid
    for orig_row, enhanced_row in zip(original_grid_blocks, enhanced_grid_blocks):
        for orig_col, enhanced_col in zip(original_grid_blocks, enhanced_grid_blocks):
            block = grid[orig_row:orig_row + block_size, orig_col:orig_col + block_size]  # Get current block
            block_key = block.tobytes()
            
            # Apply transformation if available, otherwise keep the block unchanged
            transformed_block = transformations.get(block_key, None)
            
            # If no transformation is found, resize the block to fit the enhanced grid dimensions
            if transformed_block is None:
                transformed_block = np.pad(block, ((0, new_block_size - block_size), (0, new_block_size - block_size)), mode='constant')

            # Place the transformed (or resized unchanged) block into the appropriate position in the new grid
            enhanced_grid[enhanced_row:enhanced_row + new_block_size, enhanced_col:enhanced_col + new_block_size] = transformed_block
    
    return enhanced_grid


def count_active_cells(part):
    """
    Solves the puzzle by iteratively enhancing the grid for a specified number of iterations.
    Returns the count of active cells (True values) in the final grid.
    """
    # Convert the initial grid pattern into a NumPy array
    grid = convert_to_numpy(initial_grid_pattern)
    # Set the number of iterations based on the puzzle part
    iterations = 5 if part == 1 else 18

    # Enhance the grid for the specified number of iterations
    for _ in range(iterations):
        grid = enhance_grid(grid)

    # Count and return the number of active cells in the final grid
    return int(grid.sum())


# Solve for both parts of the puzzle
print("Part 1 solution:", count_active_cells(part=1))
print("Part 2 solution:", count_active_cells(part=2))
