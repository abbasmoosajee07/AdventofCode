# Advent of Code - Day 5, Year 2022
# Solution Started: Nov 28, 2024
# Puzzle Link: https://adventofcode.com/2022/day/5
# Solution by: [abbasmoosajee07]
# Brief: [Moving Crates]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D05_file = "Day05_input.txt"
D05_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D05_file)

# Read and sort input data into a grid
with open(D05_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    stacks_init = input_data[0].split('\n')
    movement_list = input_data[1].split('\n')

def create_stack(stacks):
    split_stack = [list(line) for line in stacks]
    transposed_stack = np.transpose(split_stack)
    stack_dict = {}
    for line in transposed_stack:
        row_no = line[-1]
        if row_no.isdigit():
            crates = ''.join(line[:-1][::-1]).replace(" ","")
            stack_dict[int(row_no)] = list(crates)
    return stack_dict

def move_crates(stacks, num_crates, source_stack, destination_stack, order = 'reverse'):
    # Create a deep copy of the stacks to avoid modifying the original
    updated_stacks = copy.deepcopy(stacks)

    # Get the source stack and the crates to move
    source_crates = updated_stacks[source_stack]
    crates_to_move = source_crates[-num_crates:]

    # Remove the crates from the source stack
    del source_crates[-num_crates:]

    # Get the destination stack and add the moved crates
    destination_crates = updated_stacks[destination_stack]
    if order == 'original':
        updated_destination = destination_crates + crates_to_move
    elif order == 'reverse':
        updated_destination = destination_crates + crates_to_move[::-1]

    # Update the stacks with the modified source and destination
    updated_stacks[source_stack] = source_crates
    updated_stacks[destination_stack] = updated_destination

    return updated_stacks

def make_all_moves(stacks_init, movement_list, order = 'reverse'):
    current_stack = stacks_init
    for move in movement_list:
        no_crates, from_stack, to_stack = map(int, re.findall(r'\d+', move))
        current_stack = move_crates(current_stack, no_crates, from_stack, to_stack, order)
    return current_stack

def find_top_crate(stacks):
    top_crates = []
    for key in stacks:
        col_stack = stacks[key]
        top_crates.append(col_stack[-1])
    return ''.join(top_crates)

stack_array = create_stack(stacks_init)
stacks_p1 = make_all_moves(stack_array, movement_list, order = 'reverse')
ans_p1 = find_top_crate(stacks_p1)
print("Part 1:", ans_p1)

stacks_p2 = make_all_moves(stack_array, movement_list, order = 'original')
ans_p2 = find_top_crate(stacks_p2)
print("Part 2:", ans_p2)