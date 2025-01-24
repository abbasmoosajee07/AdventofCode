"""Advent of Code - Day 11, Year 2019
Solution Started: Jan 23, 2025
Puzzle Link: https://adventofcode.com/2019/day/11
Solution by: abbasmoosajee07
Brief: [Intcode Painting Robots]
"""

#!/usr/bin/env python3

import os, re, copy, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)

from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = list(map(int, input_data))

def run_robot(robot_program: list[int], base_color: int):
    robot_cpu = Intcode_CPU(robot_program, base_color, debug=False)
    robot_cpu.process_program()
    robot_output = robot_cpu.get_result('output')
    robot_instructions = list(zip(robot_output[::2], robot_output[1::2]))
    print(robot_instructions)
    tiles_dict = {}
    for color, direction in robot_instructions:
        print(color, direction)
    return tiles_dict

output = run_robot(input_program, 1)
print("Output:", sum(output))
