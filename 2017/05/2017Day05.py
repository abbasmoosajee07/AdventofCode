# Advent of Code - Day 5, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/5
# Solution by: [abbasmoosajee07]
# Brief: [Jumping number lists]

import os
import numpy as np

# Load the input file
D5_file = 'Day05_input.txt'
D5_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D5_file)

with open(D5_file_path) as file:
    input_data = file.read().splitlines()
    input_data = np.array(input_data, dtype=int)

    # Make a copy of the original input for both parts
    input1 = input_data.copy()
    input2 = input_data.copy()

# Part 1: Original algorithm
def leave_list(instruction_list):
    pos = 0
    steps = 0

    while 0 <= pos < len(instruction_list):
        jump = instruction_list[pos]
        instruction_list[pos] += 1
        pos += jump
        steps += 1
        
    return steps

# Part 2: Modified algorithm with decrement for jumps >= 3
def leave_list2(instruction_list):
    pos = 0
    steps = 0

    while 0 <= pos < len(instruction_list):
        jump = instruction_list[pos]
        if jump >= 3:
            instruction_list[pos] -= 1
        else:
            instruction_list[pos] += 1
        pos += jump
        steps += 1
        
    return steps

# Run Part 1
P1_step_count = leave_list(input1.copy())
print(f"Part 1: Number of steps required to leave: {P1_step_count}")

# Run Part 2
P2_step_count = leave_list2(input2.copy())
print(f"Part 2: Number of steps required to leave: {P2_step_count}")

