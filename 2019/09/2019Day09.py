# Advent of Code - Day 9, Year 2019
# Solution Started: Nov 18, 2024
# Puzzle Link: https://adventofcode.com/2019/day/9
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer v4.0]

#!/usr/bin/env python3

import os, sys
intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)

from Intcode_Computer import Intcode_CPU
# Load the input data from the specified file path
D09_file = "Day09_input.txt"
D09_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D09_file)

# Read and parse input data into a list of integers
with open(D09_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

# Part 1: Execute the Intcode program with input 1
cpu_p1 = Intcode_CPU(input_program, inputs = 1)
cpu_p1.process_program()
boost_code = cpu_p1.get_result('output')
print("Part 1:", boost_code[0])

# Part 2: Execute the Intcode program with input 2
cpu_p2 = Intcode_CPU(input_program, inputs = 2)
cpu_p2.process_program()
distress_coords = cpu_p2.get_result('output')
print("Part 1:", distress_coords[0])
