# Advent of Code - Day 2, Year 2021
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2021/day/2
# Solution by: [abbasmoosajee07]
# Brief: [Submarine Navigations]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D02_file = "Day02_input.txt"
D02_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D02_file)

# Read and sort input data into a grid
with open(D02_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_instructions(instructions):
    instruction_list = []
    for line in instructions:
        command, magnitude = line.split(' ')
        instruction_list.append([command, int(magnitude)])
    return instruction_list

def navigate_submarine(command_list, start = (0, 0)):
    x, y = start
    for command, magnitude in command_list:
        if command == 'forward':
            x += magnitude
        elif command == 'down':
            y += magnitude
        elif command == 'up':
            y -= magnitude
    return x * y

def navigate_aim_submarine(command_list, start = (0, 0, 0)):
    x, y, aim = start
    for command, magnitude in command_list:
        if command == 'down':
            aim += magnitude
        elif command == 'up':
            aim -= magnitude
        elif command == 'forward':
            x += magnitude
            y += (aim * magnitude)
    return x * y

command_list = parse_instructions(input_data)
ans_p1 = navigate_submarine(command_list)
print("Part 1:", ans_p1)

ans_p2 = navigate_aim_submarine(command_list)
print("Part 2:", ans_p2)
