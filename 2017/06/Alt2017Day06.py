# Advent of Code - Day 6, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/6
# Solution by: [abbasmoosajee07]
# Brief: [Redistribution of blocks, like candy]

import os
import numpy as np

# Load the input file
D6_file = 'Day06_input.txt'
D6_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D6_file)

with open(D6_file_path) as file:
    input_data = file.read().split()
    input_data = np.array(input_data, dtype=int)
        
    # Make a copy of the original input for both parts
    input_OG = input_data.copy()
    

def redistribute_blocks(blocks):
    
    new_blocks = blocks
    len_blocks = len(blocks)
    max_block = max(blocks)
    idx = tuple(np.argwhere(blocks == max_block).flatten())[0]
    move = 0
    new_blocks[idx] -= max_block
    
    while max_block > 0:
        
        move += 1
        pos = (idx + move) % len_blocks
        new_blocks[pos] += 1
        max_block -= 1
        
        # print(max_block, idx, pos)
    
    # print(new_blocks)
    return new_blocks

# Function to check if an array is present in the list of arrays
def array_in_list(target, array_list):
    for arr in array_list:
        if np.array_equal(arr, target):
            return True
    return False

# Initial setup
array_equal = False  # Change to False to start loop
block_input = input_OG
steps = 0
block_list = [block_input.copy()]  # Copy to avoid reference issues

while not array_equal:  # Keep looping until array is found in the list
    
    steps += 1
    print(f"Step: {steps}")
    
    # Redistribute blocks (your custom function)
    new_block = redistribute_blocks(block_input)
    
    # Check if the new block is already in the list
    array_equal = array_in_list(new_block, block_list)
    
    if not array_equal:  # Add to the list only if it's not already present
        block_list.append(new_block.copy())
    
    # Update block_input for the next loop
    block_input = new_block

print(f"Loop detected after {steps} steps.")

# Simple enough in python, but becomes really memory intensive
# as list becomes longer and needs to check against more arrays,
# taking longer. Switched to C with same structure for coode.

# Function to detect the size of the loop
def find_loop_size(blocks):
    seen_configs = {}
    steps = 0

    # Store the first configuration
    current_config = blocks.copy()
    
    while tuple(current_config) not in seen_configs:
        seen_configs[tuple(current_config)] = steps
        current_config = redistribute_blocks(current_config)
        steps += 1
    
    # When we find a repeated state, calculate the loop size
    loop_start = seen_configs[tuple(current_config)]
    loop_size = steps - loop_start

    return steps, loop_size

# Call the function to find the loop size
steps_taken, loop_size = find_loop_size(input_data)

print(f"Part 1: Total steps before loop: {steps_taken}")
print(f"Part 2: Size of the loop: {loop_size}")