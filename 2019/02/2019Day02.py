# Advent of Code - Day 2, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/2
# Solution by: [abbasmoosajee07]
# Brief: [Intcode CPU V1]

#!/usr/bin/env python3

import os, re, copy, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)

from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D02_file = "Day02_input.txt"
D02_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D02_file)

# Read and sort input data into a grid
with open(D02_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = list(map(int, input_data))


def find_address(instruction, target):
    for num_1 in range(100):  # Adjusted range to include 99
        for num_2 in range(100):
            # Set the values at positions 1 and 2
            edit_list = [(1, num_1), (2, num_2)]

            # Run the Intcode program
            cpu = Intcode_CPU(instruction)
            cpu.edit_program(edit_list)
            cpu.process_program()
            output = cpu.get_result()

            # Check if the output matches the target
            if output[0] == target:
                return num_1, num_2  # Return the values if found
    return 0, 0

cpu_p1 = Intcode_CPU(input_program)
cpu_p1.edit_program([(1, 12), (2, 2)])
cpu_p1.process_program()
ans_p1 = cpu_p1.get_result()
print("Part 1:", ans_p1[0])

noun, verb = find_address(input_program, 19690720)
print("Part 2:", (100 * noun) + verb)
