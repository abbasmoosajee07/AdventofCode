# Advent of Code - Day 2, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/2
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer V1]

#!/usr/bin/env python3

import os, re, copy, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_CPU")
sys.path.append(intcode_path)

from Intcode_CPU import Intcode_Program

# Load the input data from the specified file path
D02_file = "Day02_input.txt"
D02_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D02_file)

# Read and sort input data into a grid
with open(D02_file_path) as file:
    input_data = file.read().strip().split(',')
    input_nums = list(map(int, input_data))


def find_address(instruction, target):
    test_instructions = copy.deepcopy(instruction)
    for num_1 in range(99):
        for num_2 in range(99):
            test_instructions[1] = num_1
            test_instructions[2] = num_2

            output_p2 = Intcode_Program(test_instructions).process_program()
            if output_p2[0] == target:
                return num_1, num_2  # Fix: Return the found address
    return 0, 0  # If no valid address found

instruction_p1 = copy.deepcopy(input_nums)
instruction_p1[1] = 12
instruction_p1[2] = 2

ans_p1 = Intcode_Program(instruction_p1).process_program()
print("Part 1:", ans_p1[0])

noun, verb = find_address(input_nums, 19690720)
print("Part 2:", (100 * noun) + verb)